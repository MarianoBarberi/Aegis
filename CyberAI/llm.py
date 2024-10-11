from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

def initialize_llm(api_key=None, model="gpt-3.5-turbo-instruct", max_tokens=1000, temperature=0.0):
    # Load environment variables if api_key is not provided
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

    # Set up the OpenAI LLM
    llm = OpenAI(
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return llm

def get_template():
    return """You are a cybersecurity risk analyst at a laboratory.
    You are tasked with analyzing the risks of the laboratory's infrastructure.
    The input is a log of the laboratory's network traffic.
    Analyze the risks of the laboratory's infrastructure and score the risks from 1 to 10, 
    where 1 is the lowest risk and 5 is the highest risk.
    The output should be only in this format and no other format is accepted:
    {{
        "risk_score": 3,
        "risk_description": "The laboratory's network traffic is not encrypted.",
        "risk_mitigation": "Encrypt the laboratory's network traffic.",
        "risk_impact": "If the laboratory's network traffic is not encrypted, sensitive data can be intercepted."
    }}
    """