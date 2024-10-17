import os
from langchain_openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_llm(api_key=None, model="gpt-3.5-turbo-instruct", max_tokens=1000, temperature=0.0):
    """Initializes the OpenAI language model."""
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")

    llm = OpenAI(
        model=model,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return llm

def get_template():
    """Returns the template for the AI prompt."""
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

def analyze_row(llm, row):
    """Uses the language model to analyze a row of network traffic data."""
    template = get_template()
    input_data = f"Network traffic log: {row[1]}"
    prompt = template.replace("The input is a log of the laboratory's network traffic.", input_data)
    
    response = llm(prompt)
    return response
