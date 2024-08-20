from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

main_prompt = """
Background: You are to provide a coherent, detailed, and instruction-style solution for a cybersecurity IT engineer who is trying to remediate a vulnerability on their network. They may have advanced enterprise-level capabilities or may have to update it manually. You are not to instruct them on their individual remediation process, only on the information provided below.

Task: I want you to synthesize the following websites and instructions. Go into each of the links and read the relevant information to gather context. Synthesize these sources and information to give the correct response.

Details: Emphasize what needs to be done for the solution. Give a short and concise summary first. Cut out as much fluff as you can to maximize the efficiency of the IT worker. Do not specify internal procedural steps that depend on the maturity of the organization and may vary from company to company.

Vulnerability: 
{title}

Diagnosis: 
{diagnosis}

Consequences: 
{consequences}

Solution: 
{solution}

Vulnerability Location(s): 
{vulnerability_location}

"""

prompt = PromptTemplate.from_template(
    main_prompt
)

def generate_solution(title, diagnosis, consequences, solution, vulnerability_location):
    
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0
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
    
    return response.content



title = '3S-Smart CODESYS Gmbh Gateway Null Pointer Exception Vulnerability(ICSA-15-293-03)'

diagnosis = 'AFFECTED PRODUCTSThe following Gateway Server versions are affected:CODESYS Gateway Server, Version 2.3.9.47 and prior versions.QID Detection Logic (Authenticated)QID checks for the Vulnerable version using windows registry keys'

consequences = 'Null pointer exceptions cause the server to crash creating a denial of service.'

solution = 'Customers are advised to refer to CERT MITIGATIONS section "https://www.us-cert.gov/ics/advisories/ICSA-15-293-03" ICSA-15-293-03 for affected packages and patching details.Patch:Following are links for downloading patches to fix the vulnerabilities: "https://www.us-cert.gov/ics/advisories/ICSA-15-293-03" ICSA-15-293-03'

vulnerability_loc = """
%windir%\SysWOW64\Gateway.exe  Version is  2.3.9.38
%windir%\SysWOW64\Gateway.exe  Version is  2.3.9.32
"""

# Function with 5 inputs
# output gpt response

print(generate_solution(title, diagnosis, consequences, solution, vulnerability_loc))


