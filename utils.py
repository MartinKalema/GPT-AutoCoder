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
    
    
def write_html_css_js_to_file(plan: str, html: str, css: str, js: str) -> Optional[str]:
    """
    Write HTML, CSS, JS, and a plan to respective files.

    Args:
        plan (str): Content of the plan to write to 'plan.md'.
        html (str): Content of the HTML file to write to 'index.html'.
        css (str): Content of the CSS file to write to 'style.css'.
        js (str): Content of the JavaScript file to write to 'script.js'.

    Returns:
        Optional[str]: A success message if files are created successfully, None if an error occurs.

    Example:
        plan_content = "This is the plan."
        html_content = "<html><body><h1>Hello, World!</h1></body></html>"
        css_content = "body { background-color: lightblue; }"
        js_content = "console.log('Hello, World!');"

        result = write_html_css_js_to_file(plan_content, html_content, css_content, js_content)
        if result:
            print(result)
    """
    file_contents = {
        'plan.md': plan,
        'index.html': html,
        'style.css': css,
        'script.js': js
    }

    try:
        for filename, content in file_contents.items():
            with open(filename, 'w') as f:
                f.write(content)
    except IOError as e:
        print(f"Error writing to file: {e}")
        return None

    return "Files created successfully"