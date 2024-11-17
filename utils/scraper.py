import tldextract
import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import urljoin, urlparse
from utils import required_intents
from utils.writer import write_to_file
from utils.ibm_waston import UserPrompt, process_prompt
from utils.logger import get_logger

log = get_logger(__name__)


def extract_domain_without_tld(url):
    """
    Extracts the domain name without the TLD (Top-Level Domain).

    Args:
        url (str): The URL from which to extract the domain without TLD.

    Returns:
        str: The domain name without the TLD.
    """
    try:
        ext = tldextract.extract(url)
        return ext.domain
    except Exception as e:
        return None


def scrape_website_recursive(
    url: str,
    visited: set = None,
    aggregated_content: str = "",
) -> tuple:
    """
    Recursively scrape all pages linked from the given URL and append content to a single file.

    Args:
        url (str): The starting URL of the website.
        visited (set): A set to keep track of visited URLs to avoid duplication.
        aggregated_content (str): Accumulated content from all pages.

    Returns:
        tuple: A tuple containing:
            - The aggregated content from all the pages scraped.
            - The main title of the website.
    """
    if visited is None:
        visited = set()

    if url in visited:
        log.info(f"Already visited: {url}")
        return aggregated_content, None

    log.info(f"Scraping URL: {url}")
    visited.add(url)

    try:
        # Make a GET request to fetch the content of the page
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code != 200:
            log.error(
                f"Failed to fetch URL: {url}. Status code: {response.status_code}"
            )
            return aggregated_content, None

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract page title
        title = soup.title.string.strip() if soup.title else "Untitled_Page"

        # Extract all text content
        paragraphs = soup.find_all("p")
        page_content = " ".join([para.get_text().strip() for para in paragraphs])

        # Page content
        pg_content = f"Title: {title}\n{page_content}\n\n"

        # Aggregate the content from this page
        aggregated_content += pg_content

        # Find all links on the page
        links = {urljoin(url, a["href"]) for a in soup.find_all("a", href=True)}

        # Filter links to include only those in the same domain and exclude unwanted types
        domain = urlparse(url).netloc
        links = {
            link
            for link in links
            if urlparse(link).netloc == domain
            and not any(
                link.endswith(ext) for ext in (".jpg", ".png", ".gif", ".jpeg", ".bmp")
            )
        }

        # Recursively scrape each link
        for link in links:
            if link not in visited:
                aggregated_content, _ = scrape_website_recursive(
                    link, visited, aggregated_content
                )

    except requests.RequestException as e:
        log.error(f"Request error while fetching URL: {url}. Error: {e}")
    except Exception as e:
        log.error(f"Unexpected error while scraping URL: {url}. Error: {e}")

    if len(title) > 64:
        title = extract_domain_without_tld(url)

    return aggregated_content, title


def fetch_and_summarize_content(url: str):
    """
    Scrapes the content of the provided URL and generates a summary.
    Args:
        url (str): The URL to scrape and summarize.
    Returns:
        tuple: A tuple containing the summarized content and the website title.
    """
    content, title = scrape_website_recursive(url)

    if not content:
        log.error("Failed to fetch content from the provided URL.")
        return None, None

    prompt = UserPrompt(
        text=f""""
        Ensure to provide a detailed summary of the following content, highlighting the {', '.join(required_intents)}: {content}\n.

        Please return your response in the Markdown format. Only use the english language.
        """
    )
    summary = process_prompt(prompt)

    if not summary:
        log.error("Failed to summarize the website content.")
        return None, None

    return summary, title


def save_summary_markdown(data, filename):
    """
    Save the website summary as a markdown file and provide a Streamlit download link.

    Args:
        summary (str): Summarized content of the website.
        workspace_name (str): Name of the workspace (used for the filename).
    """
    file_path = write_to_file(data, filename, file_type="md")
    st.info(f"File saved successfully: `{file_path}`")
