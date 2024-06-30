import tenacity
import os
import openai
from termcolor import colored
from utils import read_yaml_file
from dotenv import load_dotenv

load_dotenv()

print(colored("Welcome to the Full Stack Web Developer Assistant", "green"))
print(colored("!!! DELETE HTML, CSS, & JS FILES IF YOU WANT THE ASSISTANT TO START FROM SCRATCH !!!", "red"))

instruction = input("Press any key to continue or type 'exit' to exit")

if instruction.strip().lower() == "exit":
    exit()

yaml_contents = read_yaml_file('params.yml')

model = yaml_contents['MODEL']