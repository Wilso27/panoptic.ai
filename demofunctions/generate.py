from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

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


def get_vuln_info(vuln_id):
    # read in as a csv and return the row with the vuln_id 
    pass



def generate_solution(title, diagnosis, consequences, solution, vulnerability_location):
    
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.01
    )
    
    chain = (
        prompt
        | model
    )
    
    # response = chain.invoke(
    #     {
    #         "title": title,
    #         "diagnosis": diagnosis,
    #         "consequences": consequences,
    #         "solution": solution,
    #         "vulnerability_location": vulnerability_location
    #     }
    # )
    
    # return response.content
    return "test"