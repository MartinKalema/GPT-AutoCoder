import yaml
from typing import Optional, Any

def read_yaml_file(file_path: str) -> Optional[Any]:
    """
    Read YAML data from a file and return it as Python objects.

    Args:
        file_path (str): Path to the YAML file to be read.

    Returns:
        Optional[Any]: Python objects representing the YAML data, or None if there was an error.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        yaml.YAMLError: If there is an error in parsing the YAML file.

    Example:
        If you have a YAML file 'example.yaml' with contents:
        ```
        key1: value1
        key2: value2
        ```
        You can read it and print its contents as follows:

        ```python
        yaml_file_path = 'example.yaml'
        yaml_data = read_yaml_file(yaml_file_path)
        if yaml_data:
            print("YAML data:")
            print(yaml_data)
        ```

    """

    try:
        with open(file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            return yaml_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file {file_path}: {e}")
        return None