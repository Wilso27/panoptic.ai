
from dotenv import load_dotenv
load_dotenv(dotenv_path='backend/.env.local')
from typing import Type
from time import time
import warnings
warnings.filterwarnings(
    "ignore",
    message="`clean_up_tokenization_spaces` was not set. It will be set to `True` by default."
)

# Langchain imports
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import sys
sys.path.append('backend/chatbot')
from llm_processor import LLMProcessor

from system_prompts import *

class ConversationManager:
    def __init__(self, 
                 langchain_model_class: Type=ChatGroq,
                 model_name: str="llama3-8b-8192",
                 header: dict=None,
                 system_message: str="",
                 temperature: int=0,
                 with_structure: Type=None,  # Pydantic model for if you are using structured output
                 # TODO: Add more settings here
                 return_time=False,
                 ):
        
        # TODO: Make robust handling so different types of langchain_model_class will have valide model_name
        self._validate_model_name(langchain_model_class, model_name)
        
        self.langchain_model_class = langchain_model_class
        self.model_name = model_name
        self.header = header
        self.system_message = system_message
        self.temperature = temperature
        self.with_structure = with_structure
        self.session_id = str(time())  # Generate a unique session ID
        self.return_time = return_time
        
        # Initialize the LLM
        self.llm = LLMProcessor(langchain_model_class=self.langchain_model_class, model_name=self.model_name, 
                                header=self.header, system_message=self.system_message, 
                                temperature=self.temperature, with_structure=self.with_structure, 
                                session_id=self.session_id, return_time=self.return_time)

        # user_input = "**AI INTRODUCE YOURSELF**"
        # self.llm.process(user_input)
        user_input = ""
        
        while 'goodbye' not in user_input.lower():
            user_input = input("You: ")
            self.llm.process(user_input)
        
        
    def _validate_model_name(self, langchain_model_class, model_name):
        if langchain_model_class == ChatGroq:
            assert model_name in ["llama-3.1-8b-instant", "llama-3.1-70b-versatile"], \
                "Invalid model_name for ChatGroq. Choose from 'llama-3.1-8b-instant', 'llama-3.1-70b-versatile'."
        elif langchain_model_class == ChatOpenAI:
            assert model_name in ["gpt-3.5-turbo", "gpt-4o"], \
                "Invalid model_name for ChatOpenAI. Choose from 'gpt-3.5-turbo', 'gpt-4o'."
        else:
            raise ValueError("Invalid langchain_model_class. Choose from ChatGroq, ChatOpenAI.")
        

if __name__ == "__main__":
    # username = input("What is your name? ")
    # company_name = input("What is the name of your company? ")
    title = "Title"
    diagnosis = "Diagnosis"
    consequences = "Consequences"
    solution = "Solution"
    vulnerability_location = "Vulnerability Location"
    generated_solution = "Generated Solution"
    
    system_prompt = vulnerability_chat_prompt.format(title=title, diagnosis=diagnosis, 
                                                       consequences=consequences, solution=solution, 
                                                       vulnerability_location=vulnerability_location, generated_solution=generated_solution)
    
    # Start the conversation manager
    ConversationManager(ChatGroq, 
                        model_name="llama-3.1-70b-versatile",  # llama-3.1-8b-instant, llama-3.1-70b-versatile
                        system_message=system_prompt, 
                        return_time=True)  # True prints the time it took to generate the response

