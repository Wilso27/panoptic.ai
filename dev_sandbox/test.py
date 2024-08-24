from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import markdown2
import re
from flask import Flask, render_template, request
import pandas as pd
df = pd.read_csv('demodata/vuln_list.csv')



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


def generate_solution(title, diagnosis, consequences, solution, vulnerability_location):
    
    model = ChatGroq(
        model="llama-3.1-70b-versatile",  # gpt-4o
        temperature=0.01
    )
    
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
    # Replace URLs with markdown links
    response_content = response.content
    response_content = re.sub(r'(https?://[^\s]+)', r'[see link](\1)', response_content)

    return response_content



title = '3S-Smart CODESYS Gmbh Gateway Null Pointer Exception Vulnerability(ICSA-15-293-03)'

diagnosis = 'AFFECTED PRODUCTSThe following Gateway Server versions are affected:CODESYS Gateway Server, Version 2.3.9.47 and prior versions.QID Detection Logic (Authenticated)QID checks for the Vulnerable version using windows registry keys'

consequences = 'Null pointer exceptions cause the server to crash creating a denial of service.'

solution = 'Customers are advised to refer to CERT MITIGATIONS section "https://www.us-cert.gov/ics/advisories/ICSA-15-293-03" ICSA-15-293-03 for affected packages and patching details.Patch:Following are links for downloading patches to fix the vulnerabilities: "https://www.us-cert.gov/ics/advisories/ICSA-15-293-03" ICSA-15-293-03'

vulnerability_loc = r"""
%windir%\SysWOW64\Gateway.exe  Version is  2.3.9.38
%windir%\SysWOW64\Gateway.exe  Version is  2.3.9.32
"""

# Function with 5 inputs
# output gpt response

response = generate_solution(title, diagnosis, consequences, solution, vulnerability_loc)
print(response)