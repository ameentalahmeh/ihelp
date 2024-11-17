import os
import json
import streamlit as st
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from utils import required_intents
from utils.prompt_processor import UserPrompt, process_prompt
from utils.parser import parse_json_code
from utils.writer import write_to_file
from utils.logger import get_logger


# Initialize the logger
log = get_logger(__name__)

# IBM Watson Assistant Credentials
API_KEY = os.getenv("ASSISTANT_APIKEY")  # Fetch from .env file
SERVICE_URL = os.getenv("ASSISTANT_URL")  # Fetch from .env file

# Check if environment variables are loaded correctly
if not API_KEY or not SERVICE_URL:
    st.error("IBM API Key or Service URL not set in the environment variables.")
    exit(1)

# Setup the authenticator and Watson Assistant client
authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV1(
    version="2021-06-14",  # Use the correct Watson API version
    authenticator=authenticator,
)
assistant.set_service_url(SERVICE_URL)


def list_workspaces():
    """
    Lists all available Watson Assistant workspaces.

    Returns:
        list: A list of dictionaries representing the available workspaces, each containing 'workspace_id', 'name', and 'description'.
    """
    try:
        response = assistant.list_workspaces().get_result()
        workspaces = response.get("workspaces", [])
        formatted_workspaces = [
            {
                "id": workspace.get("workspace_id"),
                "name": workspace.get("name"),
                "description": workspace.get("description", "No description provided"),
            }
            for workspace in workspaces
        ]
        return formatted_workspaces
    except Exception as e:
        log.error(f"Error listing workspaces: {e}")
        return []


def delete_workspace(workspace_id: str):
    """
    Deletes a Watson Assistant workspace.

    Args:
        workspace_id (str): The ID of the workspace to delete.

    Returns:
        bool: True if the workspace was successfully deleted, False otherwise.
    """
    try:
        assistant.delete_workspace(workspace_id=workspace_id).get_result()
        log.info(f"Workspace {workspace_id} deleted successfully.")
        return True
    except Exception as e:
        log.error(f"Error deleting workspace {workspace_id}: {e}")
        return False


def create_workspace(site_title: str, site_description: str):
    """
    Creates a Watson Assistant workspace dynamically using the site title and description.
    Args:
        site_title (str): The title of the website.
        site_description (str): A description of the website.
    """
    response = assistant.create_workspace(
        name=site_title,
        description=site_description,
        language="en",
    ).get_result()

    workspace_id = response["workspace_id"]
    return workspace_id


def fetch_workspace_details(workspace_id):
    """
    Fetch the details of the selected workspace by its ID.

    Args:
        workspace_id (str): The ID of the workspace.
    """
    # Replace with actual API call to fetch workspace details
    workspaces = list_workspaces()
    for ws in workspaces:
        if ws["id"] == workspace_id:
            return ws
    return None


def get_intents_and_actions(summary: str) -> tuple:
    """
    Fetches predefined intents and actions, then sends website summary, current intents, and actions to the LLM
    to complete unanswered intents and generate additional intents and actions based on the website details.

    Args:
        summary (str): The summarized content of the website.

    Returns:
        tuple: A tuple containing the updated intents and actions.
    """
    # Directories for predefined intents and actions
    intents_dir = "samples/intents"
    actions_dir = "samples/actions"

    predefined_intents = []
    predefined_actions = []

    # Process predefined intents
    for filename in os.listdir(intents_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(intents_dir, filename)
            with open(file_path, "r") as f:
                content = json.load(f)
                if isinstance(content, list):  # Ensure it's a list
                    predefined_intents.extend(content)  # Add all intents to the list

    # Process predefined actions
    for filename in os.listdir(actions_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(actions_dir, filename)
            with open(file_path, "r") as f:
                content = json.load(f)
                if isinstance(content, list):  # Ensure it's a list
                    predefined_actions.extend(content)  # Add all actions to the list

    # Construct the prompt to ask the LLM to complete the intents and actions
    prompt = UserPrompt(
        text=f"""
        I have a website summary and a list of intents and actions for an IBM Watson Assistant. 
        Please help complete the unanswered intents (like {', '.join(required_intents)}), 
        add new intents based on the website content, and create actions for these specific intents if they do not have actions yet. 
        Do not repeat existing intents or actions.

        Website Summary: {summary}

        Current Intents: {json.dumps(predefined_intents, indent=2)}

        Current Actions: {json.dumps(predefined_actions, indent=2)}

        Ensure actions are generated for the following intents if they do not already have actions: {', '.join(required_intents)}

        Please return your response in the following format:

        {{
            "new_intents": [...],
            "new_actions": [...],
        }}

        Provide ONLY new intents and actions based on the website content, and add actions for the required intents {', '.join(required_intents)} if they are missing. 
        Do not include a prefix like 'Here is the response:' before the JSON, as it interferes with JSON extraction and parsing.
        """
    )

    # Process the prompt to get the response from the LLM
    completed_response = process_prompt(prompt)

    # If the LLM fails to provide a valid response, return the original intents and actions
    if not completed_response:
        st.error("Failed to generate or complete intents and actions.")
        return predefined_intents, predefined_actions

    # Extract the updated intents and actions from the LLM response (assume it's a JSON-like string)
    try:
        # Parse the completed response from LLM to get new intents and actions
        updated_data = parse_json_code(completed_response)

        # Retrieve new intents and actions or fallback to current intents/actions
        new_intents = updated_data.get("new_intents", [])
        new_actions = updated_data.get("new_actions", [])

        # Merge new intents with the current ones, avoiding duplicates
        updated_intents = {
            intent["intent"]: intent for intent in predefined_intents
        }  # Create a dictionary for fast lookup
        for intent in new_intents:
            if intent["intent"] not in updated_intents:
                updated_intents[intent["intent"]] = (
                    intent  # Add new intent if it doesn't exist
                )

        # Convert updated_intents back to a list
        updated_intents = list(updated_intents.values())

        # Merge new actions with the current ones, avoiding duplicates
        updated_actions = {
            action["action_name"]: action for action in predefined_actions
        }  # Create a dictionary for fast lookup
        for action in new_actions:
            if action["action_name"] not in updated_actions:
                updated_actions[action["action_name"]] = (
                    action  # Add new action if it doesn't exist
                )

        # Convert updated_actions back to a list
        updated_actions = list(updated_actions.values())

    except (json.JSONDecodeError, KeyError) as e:
        log.error(f"Error processing LLM response: {e}")
        return (
            predefined_intents,
            predefined_actions,
        )  # Return the current intents and actions in case of an error

    # Return the merged updated intents and actions
    return updated_intents, updated_actions


def generate_intents_and_actions(intents: list, actions: list, workspace_id: str):
    """
    Generates intents, actions, and entities for Watson Assistant.
    Args:
        intents (list): List of user intents/inputs dictionaries.
        actions (list): List of action dictionaries to create dialog nodes.
        workspace_id (str): The Watson Assistant workspace ID.
    """
    # Create intents
    for intent in intents:
        if isinstance(intent, dict):  # Ensure each item is a dictionary
            assistant.create_intent(
                workspace_id=workspace_id,
                intent=intent.get("intent"),  # Safely access "intent"
                description=intent.get("description", ""),
                examples=intent.get("examples", []),
            )

    # Create dialog nodes (actions)
    for action in actions:
        if isinstance(action, dict):  # Ensure each item is a dictionary
            assistant.create_dialog_node(
                workspace_id=workspace_id,
                dialog_node=action.get("action_name"),  # Safely access "action_name"
                conditions=action.get("conditions", ""),
                output={"text": action.get("output_text", "")},
                title=action.get("action_name"),
                description=f"Action for {action.get('action_name', '')}",
            )


def generate_watson_workspace_json(
    intents, actions, workspace_name, workspace_description
):
    """
    Generates a Watson Assistant JSON based on categorized content and the workspace info.

    Args:
        intents (list): List of user intents/inputs dictionaries.
        actions (list): List of action dictionaries to create dialog nodes.
        workspace_name (str): Name of the workspace.
        workspace_description (str): Description of the workspace.

    Returns:
        dict: Generated Watson Assistant JSON structure.
    """

    # Generate the final Watson Assistant JSON structure
    assistant_json = {
        "intents": intents,
        "entities": [],
        "metadata": {
            "api_version": {
                "major_version": "v2",
                "minor_version": "2018:11:14",
            }
        },
        "dialog_nodes": actions,
        "counterexamples": [],
        "learning_opt_out": True,
        "language": "en",
        "description": workspace_description,
        "name": workspace_name,
    }

    return assistant_json


def save_workspace_json(data, filename):
    """
    Save JSON data to a file.

    Args:
        data (dict): JSON data to save.
        filename (str): Name of the file.
    """
    file_path = write_to_file(data, filename, file_type="json")
    st.info(f"File saved successfully: `{file_path}`")
