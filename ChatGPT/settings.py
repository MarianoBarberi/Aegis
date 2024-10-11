import streamlit as st
from llm import initialize_llm, get_template

def settings_page():
    # Load environment variables
    api_key = None  # We'll initialize this later
    model = "gpt-3.5-turbo-instruct"
    max_tokens = 1000
    temperature = 0.0

    # Set up the OpenAI LLM
    llm = initialize_llm(api_key, model, max_tokens, temperature)

    # Template for AI's response
    template = get_template()

    # AI Settings page
    st.title("AI Settings")

    # Input fields for AI configuration
    template = st.text_area("AI prompt", value=template, key="prompt")
    api_key = st.text_input("AI API key", value=api_key, key="api_key")
    model = st.text_input("AI model", value=model, key="model")
    max_tokens = st.number_input("AI max tokens", value=max_tokens, key="max_tokens", step=1)
    temperature = st.number_input("AI temperature", value=temperature, key="temperature", step=0.1)
    
    if st.button("Save"):
        # Save new settings and reinitialize the LLM
        llm = initialize_llm(api_key, model, max_tokens, temperature)
