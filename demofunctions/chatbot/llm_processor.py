
from langchain_groq import ChatGroq
from langchain_core.messages import trim_messages, HumanMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from typing import Type
from operator import itemgetter
from time import time


class LLMProcessor:
    """
    LLMProcessor is a class that processes text input and returns a response from a language model.
    """
    def __init__(self, langchain_model_class: Type=ChatGroq, 
                 model_name: str="llama3-8b-8192", header: dict=None, 
                 system_message: str="", temperature: int=0, 
                 with_structure: Type=None, session_id: str="0",
                 return_time: bool=False, 
                 ):
        
        self.langchain_model_class = langchain_model_class
        self.model_name = model_name
        self.header = header
        self.system_message = system_message
        self.temperature = temperature
        self.with_structure = with_structure
        self.session_id = session_id
        self.return_time = return_time
        
        model = langchain_model_class(
            model=model_name,
            temperature=temperature,
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_message),
                MessagesPlaceholder(variable_name="trimmed_messages"),
            ]
        )
        
        # Manage chat history
        self.store = {}
        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self.store:
                self.store[session_id] = InMemoryChatMessageHistory()  # Change this to store in a database
            return self.store[session_id]
        
        # Trim the message history to last 1024 tokens
        trimmer = trim_messages(
            max_tokens=1024,
            strategy="last",
            token_counter=model,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )
        
        # 
        chain = (
            # This gets the output from RunnableWithMessageHistory and trims it
            RunnablePassthrough.assign(trimmed_messages=itemgetter("messages") | trimmer)  # trim_messages
            | prompt  # ChatPromptTemplate
            | model  # Chat model
        )
        
        self.chat_bot = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="messages",
        )
            
    def process(self, text):
        if self.return_time is True:
            start_time = time()
        
        # Get the response from the LLM
        text_response = self.chat_bot.invoke(
            {
                "messages": [HumanMessage(content=text)], 
            },
            config={"configurable": {"session_id": self.session_id},
            },
        )
        
        if self.return_time is True:
            end_time = time()
            elapsed_time = int((end_time - start_time) * 1000)
            print(f"AI: {text_response.content}\n> LLM ({elapsed_time}ms)")
        else:
            print(f"AI: {text_response.content}")
        
        return text_response.content
