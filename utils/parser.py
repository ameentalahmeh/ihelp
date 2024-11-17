import json
from utils.logger import get_logger

log = get_logger(__name__)


def parse_json_code(json_code):
    """
    Parse a JSON string into a Python dictionary.

    Args:
        json_code (str): The extracted JSON string.

    Returns:
        dict: Parsed JSON as a Python dictionary or None if parsing fails.
    """
    try:
        parsed_json = json.loads(json_code)
        log.info("JSON successfully parsed.")
        return parsed_json
    except json.JSONDecodeError as e:
        log.error(f"JSON parsing error: {e}")
        return None
