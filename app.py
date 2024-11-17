import os
import json
import warnings
import streamlit as st
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.scraper import (
    fetch_and_summarize_content,
    save_summary_markdown,
)
from utils.ibm_waston import (
    list_workspaces,
    delete_workspace,
    create_workspace,
    get_intents_and_actions,
    generate_intents_and_actions,
    save_workspace_json,
    generate_watson_workspace_json,
)

# Load environment variables from .env file
load_dotenv()

# Initialize the logger
log = get_logger(__name__)

warnings.filterwarnings("ignore")


def display_summary(summary, title):
    """
    Display the summarized content and title in a collapsible bordered section.
    """
    st.success("Website content summarized successfully!")
    with st.expander(f"📄 Summary of {title}", expanded=True):
        st.markdown(summary)

    # Save the summary to a markdown file
    save_summary_markdown(summary, title)


def show_workspace_download_buttons(workspace_name):
    """
    Display the download buttons for markdown and JSON files after workspace is selected.

    Args:
        workspace_name (str): The selected workspace name.
    """
    filename = f"{workspace_name.lower().replace(' ', '')}_assistant"
    markdown_file_path = os.path.join("samples", "output", f"{filename}.md")
    json_file_path = os.path.join("samples", "output", f"{filename}.json")

    # Display download buttons if the markdown and JSON files exist
    if os.path.exists(markdown_file_path):
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        st.download_button(
            label="📄 Download Markdown",
            data=markdown_content,
            file_name=f"{filename}.md",
            mime="text/markdown",
        )

    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_content = json.load(f)
        st.download_button(
            label="📦 Download Watson Assistant JSON",
            data=json.dumps(json_content, indent=2),
            file_name=f"{filename}.json",
            mime="application/json",
        )


def manage_delete_workspace():
    """
    Manage workspace deletion if the maximum workspace limit is exceeded.
    """
    try:
        workspaces = list_workspaces()

        if workspaces:
            sorted_workspaces = sorted(workspaces, key=lambda ws: ws.get("created", ""))

            # Get the Latest workspace (first in sorted list)
            oldest_workspace = sorted_workspaces[4]
            selected_workspace_id = oldest_workspace["id"]
            selected_workspace_name = oldest_workspace["name"]

            with st.spinner(f"Deleting workspace: {selected_workspace_name}..."):
                try:
                    delete_workspace(selected_workspace_id)
                    st.success(
                        f"Latest workspace '{selected_workspace_name}' deleted successfully!"
                    )
                    st.rerun()
                except Exception as e:
                    log.error(f"Failed to delete workspace: {e}")
                    st.error(
                        f"An error occurred while deleting the workspace '{selected_workspace_name}'."
                    )
    except Exception as e:
        log.error(f"Error in managing workspace deletion: {e}")
        st.error("An error occurred while trying to manage workspace deletion.")


def main():
    """
    Main function for running the Streamlit app to scrape and summarize website content,
    generate IBM Watson Assistant intents and actions, and save the resulting assistant JSON.
    """

    # Configure the page with a modern title and icon
    st.set_page_config(page_title="iHelp: Your AI Assistant Builder", page_icon="🤖")

    # Add a welcoming header with visual cues
    st.title("🤖 Welcome to iHelp")
    st.caption("Your AI Assistant Builder Powered by IBM Watson")

    st.markdown(
        """
        #### 🚀 Transform Websites into AI Assistants  
        Easily convert your website into a **smart, interactive assistant** with IBM Watson.
        """,
        unsafe_allow_html=True,
    )

    # Step 1: User input for website URL
    st.markdown("### Step 1: 🌐 Enter Website URL")
    url = st.text_input("Enter the URL of your website:")

    if url:
        try:
            # Step 2: Fetch and summarize website content
            st.markdown("### Step 2: 📑 Summarize Website Content")
            with st.spinner("Fetching and summarizing website content..."):
                summary, title = fetch_and_summarize_content(url)

            if not summary:
                st.error(
                    "Unable to summarize website content. Please check the URL and try again."
                )
                return

            display_summary(summary, title)

            # Step 3: Create a Watson Assistant workspace
            st.markdown("### Step 3: 🛠️ Initialize Watson Assistant Workspace")
            description = f"I'm an IBM Watson Assistant for {title}"
            with st.spinner("Creating a Watson Assistant workspace..."):
                workspace_id = create_workspace(title, description)

            st.success(f"Workspace created successfully: **{title}**")

            # Step 4: Generate intents and actions
            st.markdown("### Step 4: 🤖 Generate Intents and Actions")
            with st.spinner("Generating intents and actions..."):
                intents, actions = get_intents_and_actions(summary)
                generate_intents_and_actions(
                    intents=intents, actions=actions, workspace_id=workspace_id
                )

            st.success("Intents and actions generated successfully!")

            # Step 5: Generate the Watson Assistant JSON
            st.markdown("### Step 5: 📦 Generate Watson Assistant JSON")
            with st.spinner("Generating JSON structure..."):
                assistant_json = generate_watson_workspace_json(
                    intents=intents,
                    actions=actions,
                    workspace_name=title,
                    workspace_description=description,
                )

            # Step 6: Save and provide download link for the Watson Assistant JSON
            save_workspace_json(data=assistant_json, filename=title)

            # Show action buttons
            show_workspace_download_buttons(workspace_name=title)

        except Exception as e:
            log.error(f"An error occurred: {e}")
            st.error(e.message)

            # Check if maximum workspaces limit exceeded
            if "Maximum workspaces limit exceeded" in str(e):
                manage_delete_workspace()


if __name__ == "__main__":
    main()
