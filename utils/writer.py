import os
import json
from utils.logger import get_logger

log = get_logger(__name__)


def write_to_file(data, filename: str, file_type="md"):
    """
    Save data to a file with the specified filename and type.

    Args:
        data (dict or str): The data to save, which can be a dictionary (for JSON) or a string.
        filename (str): The name of the file to save the data in.
        file_type (str): The type of the file (default is "md", can be "json", "md").
    """
    try:
        # Ensure the output directory exists
        output_dir = "samples/output/"
        os.makedirs(output_dir, exist_ok=True)

        # Define the full file path
        file_path = os.path.join(
            output_dir, f"{filename.lower().replace(' ', '')}_assistant.{file_type}"
        )

        # Save the data to the file based on the file type
        if file_type == "json":
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        elif file_type == "md":
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(data)
        else:
            raise ValueError(
                "Unsupported file type. Supported types are 'json' and 'md'."
            )

        log.info(f"Data successfully saved to {file_path}")
        print(f"Data successfully saved to {file_path}")

        return file_path

    except ValueError as ve:
        # Handle value errors, such as unsupported file types
        log.error(f"ValueError: {ve}")
        print(f"Error: {ve}")
    except Exception as e:
        # General exception handling for unexpected errors
        log.error(f"Error saving data to file: {e}")
        print(f"Error saving data to file: {e}")
