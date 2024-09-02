from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path)

# Load the prompt from the text file
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Load the main prompt template
prompt_path = os.path.join(os.path.dirname(__file__), '..', 'demodata', 'prompt_template.txt')
main_prompt = load_prompt(prompt_path)

# Create a prompt template from the loaded prompt
prompt = ChatPromptTemplate.from_template(main_prompt)

# Initialize the chat model
model = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.01)

def generate_solution(title, diagnosis, consequences, solution, vulnerability_location, previous_messages=None):
    if previous_messages is None:
        previous_messages = []

    # Build the context by combining previous messages
    context = "\n".join([f"Human: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}" for msg in previous_messages])

    # Construct the input for the model
    input_text = f"{context}\nHuman: Title: {title}\nDiagnosis: {diagnosis}\nConsequences: {consequences}\nSolution: {solution}\nVulnerability Location: {vulnerability_location}\nAI:"

    # Invoke the model
    response = None
    for _ in range(5):
        try:
            response = model([HumanMessage(content=input_text)])
            break
        except Exception as e:
            print(f"Error: {e}. Retrying...")

    # Process the response
    if response:
        response_content = response.content
        response_content = re.sub(r'(https?://[^\s]+)', r'[see link](\1)', response_content)
        # Append the AI's response to the conversation history
        previous_messages.append(AIMessage(content=response_content))
        return response_content, previous_messages
    else:
        return "Failed to generate a response after multiple attempts.", previous_messages

# Example usage
if __name__ == "__main__":
    # Initial setup
    title = '3S-Smart CODESYS Gmbh Gateway Null Pointer Exception Vulnerability (ICSA-15-293-03)'
    diagnosis = 'AFFECTED PRODUCTS The following Gateway Server versions are affected: CODESYS Gateway Server, Version 2.3.9.47 and prior versions. QID Detection Logic (Authenticated) QID checks for the Vulnerable version using windows registry keys'
    consequences = 'Null pointer exceptions cause the server to crash creating a denial of service.'
    solution = 'Customers are advised to refer to CERT MITIGATIONS section "https://www.us-cert.gov/ics/advisories/ICSA-15-293-03" ICSA-15-293-03 for affected packages and patching details. Patch: Following are links for downloading patches to fix the vulnerabilities: "https://www.us-cert.gov/ics/advisories/ICSA-15-293-03" ICSA-15-293-03'
    vulnerability_loc = r"%windir%\SysWOW64\Gateway.exe  Version is  2.3.9.38\n%windir%\SysWOW64\Gateway.exe  Version is  2.3.9.32"

    # Empty list to hold previous messages (conversation history)
    conversation_history = []

    # Generate the first solution
    response, conversation_history = generate_solution(
        title, diagnosis, consequences, solution, vulnerability_loc, conversation_history
    )
    print("First Response:\n", response)

    # Continue the conversation
    user_input = "Can you provide more details on the consequences?"
    conversation_history.append(HumanMessage(content=user_input))
    response, conversation_history = generate_solution(
        title, diagnosis, consequences, solution, vulnerability_loc, conversation_history
    )
    print("Follow-up Response:\n", response)
