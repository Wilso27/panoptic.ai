from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

# Get the path to the .env file and load it
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path)

# Load the prompt from the text file
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
# Load the prompt from the text file
prompt_path = os.path.join(os.path.dirname(__file__), '..', 'demodata', 'prompt_template.txt')
main_prompt = load_prompt(prompt_path)

# Create a prompt template from the loaded prompt
prompt = PromptTemplate.from_template(
    main_prompt
)

# Define the model
model = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.01)

def generate_solution(title, diagnosis, consequences, solution, vulnerability_location):
    chain = (
        prompt
        | model
    )
    
    response = chain.invoke(
        {
            "title": title,
            "diagnosis": diagnosis,
            "consequences": consequences,
            "solution": solution,
            "vulnerability_location": vulnerability_location
        }
    )
    # Replace URLs with markdown links and get other regex formatting
    response_content = response.content
    response_content = re.sub(r'(https?://[^\s]+)', r'[see link](\1)', response_content)
    response_content = re.sub(r"(\*\*[^:]+:\*\*)\s*(?=\S)", r"\1\n", response_content)
    response_content = re.sub(r"(\*\*Remediation Steps:\*\*)\s*(?=\S)", r"\1\n\n", response_content)
    return response_content
