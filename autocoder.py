import tenacity
import os
from openai import OpenAI
from termcolor import colored
from utils import read_yaml_file, write_html_css_js_to_file
import json
from typing import Dict

client = OpenAI(api_key= os.environ.get("OPENAI_API_KEY"))

# prompt user
print(colored("Welcome to the Full Stack Web Developer Assistant", "green"))
print(colored("WARNING: Deleting HTML, CSS, & JS files will reset the assistant to start from scratch.", "red"))


instruction = input("Press any key to continue or type 'exit' to exit")
if instruction.strip().lower() == "exit":
    exit()

# load params
yaml_contents = read_yaml_file('params.yml')

# returns code
@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10), stop=tenacity.stop_after_attempt(4), reraise=True,)
def return_code_and_user_input(model: str) -> Dict[str, str]:
    """
    Prompt the user for input, capture it, and interact with an AI model to generate code files.

    Args:
        model (str): The name or identifier of the AI model to use.

    Returns:
        Dict[str, str]: A dictionary containing the arguments for the 'write_html_css_js_to_file' function,
                       including 'plan', 'html', 'css', and 'js' code strings.

    Example:
        result = return_code("my_model")
        if result:
            print("Function arguments:", result)
    """
    entry = ''

    print(colored("\n NOTE: This input accepts multiple lines. Feel free to provide as much detail as you'd like.", "green"))
    print(colored("What type of website can I code for you? (Type 'done' on a new line and press 'enter' when finished.)", "yellow"))

    while True:
        response = input()
        if response.strip().lower() == 'done':
            break

        entry += response + '\n'

    print(colored("Starting to code...", "green"))

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{yaml_contents['SYSTEM_PROMPT_ONE']['MESSAGE']}"},
            {"role": "user", "content": f"{entry}"},
        ],
        function_call={"name": "write_html_css_js_to_file"},
        functions=[
            {
                "name": "write_html_css_js_to_file",
                "description": "This function takes in html, css, js and writes them to their respective files",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan": {
                            "type": "string",
                            "description": "Your detailed plan in markdown to solve errors or improve code to be written to plan file",
                        },
                        "html": {
                            "type": "string",
                            "description": "The html code to be written to html file",
                        },
                        "css": {
                            "type": "string",
                            "description": "The css code to be written to css file",
                        },
                        "js": {
                            "type": "string",
                            "description": "The js code to be written to js file",
                        },
                    },
                    "required": ["plan", "html", "css", "js"]
                }
            }
        ]
    )

    if response.choices[0].message.function_call:
        function_args = json.loads(response.choices[0].message.function_call.arguments)
        return function_args, entry
    else:
        print(colored(response.choices[0].message.content))

    return {}

# create files
if not os.path.exists('index.html'):
    function_args, previous_user_input = return_code_and_user_input(yaml_contents['MODEL'])
    write_html_css_js_to_file(**function_args)

# code improvement vars
x = 1
number_of_autonomous_runs_without_user_feedback = 1
retry_due_to_error = False

while True:
    # retrieve code to be improved
    previous_plan = open('plan.md').read()
    previous_html = open('index.html').read()
    previous_css = open('style.css').read()
    previous_js = open('script.js').read()

    if retry_due_to_error:
        entry = previous_user_input
    elif x % number_of_autonomous_runs_without_user_feedback == 0:
        entry = ''

        print(colored("\n NOTE: This input accepts multiple lines. Feel free to provide as much detail as you'd like.", "green"))
        print(colored("What type of improvements do you want for this website? (Type 'done' on a new line and press 'enter' when finished.)", "yellow"))

        while True:
            response = input()

            if response.strip().lower() == 'done':
                break

            entry += response + '\n'
    else:
        entry = yaml_contents['IMPROVEMENT_PROMPT']['MESSAGE']

