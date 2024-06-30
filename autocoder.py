import tenacity
import os
from openai import OpenAI
from termcolor import colored
from utils import read_yaml_file
import json

client = OpenAI(api_key= os.environ.get("OPENAI_API_KEY"))

# prompt user
print(colored("Welcome to the Full Stack Web Developer Assistant", "green"))
print(colored("!!! DELETE HTML, CSS, & JS FILES IF YOU WANT THE ASSISTANT TO START FROM SCRATCH !!!", "red"))

instruction = input("Press any key to continue or type 'exit' to exit")
if instruction.strip().lower() == "exit":
    exit()

# load params
yaml_contents = read_yaml_file('params.yml')
model = yaml_contents['MODEL']
SP1 = yaml_contents['SYSTEM_PROMPT_ONE']['MESSAGE']

# returns code
@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10), stop=tenacity.stop_after_attempt(4), reraise=True,)
def return_code(model):

    entry = ''

    print(colored("\n NOTE: This is a multiline input, you can write as much detail as you want in here.", "green"))
    print(colored("What type of website can i code for you? (Type 'done' on a new line and press 'enter' when you are done)", "yellow"))

    while True:
        response = input()
        if response.strip().lower() == 'done':
            break

        entry = response + '\n'
    print(colored("Starting to code...", "green"))


    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{SP1}"},
            {"role": "user", "content": f"{entry}"},
        ],
        # max_tokens=2000,
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
                        }
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
        ]
    )

    if response.choices[0].message.function_call:
        function_args = json.loads(response.choices[0].message.function_call.arguments)
        return function_args
    else:
        print(colored(response.choices[0].message.content))

