from langchain.chat_models import ChatOpenAI
import os
import re

chat = ChatOpenAI(openai_api_key=os.environ.get("GPT_KEY"))

def write_string_to_file(filename, string, mode):
    with open(filename, mode) as file:
            file.write(f"\n{string}\n")
    return file

def read_string_from_file(path):
    with open(path, 'r') as file:
            text = file.read()
    return text

def read_prompt(classifier, param):
    prompt_path = f"ara/{classifier}/{param}.data/{classifier}.prompt"
    try:
        prompt = read_string_from_file(prompt_path)
    except FileNotFoundError:
        exception_message_file_path = f"{param}.data/{classifier}.prompt"
        print(f"ERROR: {exception_message_file_path} does not exist. No prompt will be executed")
        return
    return prompt

def send_prompt(prompt):
    chat_result = chat.invoke(prompt)
    return chat_result.content

def append_headings(classifier, param, heading_name):
    artefact_data_path = f"ara/{classifier}/{param}.data/{classifier}_exploration.md"
    content = read_string_from_file(artefact_data_path)
    pattern = r'## {}_(\d+)'.format(heading_name)
    matches = re.findall(pattern, content)

    max_number = 1
    if matches:
        max_number = max(map(int, matches)) + 1
    heading = f"## {heading_name}_{max_number}"
            
    write_string_to_file(artefact_data_path, heading, 'a')

def write_prompt_result(classifier, param, text):
    artefact_data_path = f"ara/{classifier}/{param}.data/{classifier}_exploration.md"
    write_string_to_file(artefact_data_path, text, 'a')
