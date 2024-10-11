import streamlit as st
from llm import initialize_llm, get_template
import json
import matplotlib.pyplot as plt


def home_page():
    response = None
    # Initialize the LLM
    llm = initialize_llm()

    # Template for AI's response
    template = get_template()

    # Streamlit app title
    st.title("Análisis de Riesgos")

    # Input field for user queries (e.g., logs or risk descriptions)
    # Example
    # Multiple failed login attempts detected on server 10.0.0.5.
    user_input = st.text_area("Paste network log or describe event:", "")

    if user_input:
        # Prepare the prompt by filling it with user input
        final_prompt = template + f"\nInput: {user_input}"
        
        # Get the response from the LLM
        response = llm.invoke(final_prompt)
        
        # Standardize the response
        response = response[response.find('{'):]

    if response:
        dummy_input = "Network traffic is not encrypted."
        dummy_response = """
        {
            "risk_score": 3,
            "risk_description": "Network traffic is not encrypted.",
            "risk_mitigation": "Encrypt the laboratory's network traffic.",
            "risk_impact": "If the laboratory's network traffic is not encrypted, sensitive data can be intercepted."
        }"""


        st.subheader("Analysis Result")
        st.table({
            "Input": [user_input, dummy_input],
            "Response": [response, dummy_response]
        })

        st.subheader("Risk Score Bar Graph")
        fig, ax = plt.subplots()
        try:
            data_dict = json.loads(response)
            ax.bar([user_input], [data_dict['risk_score']], color='blue')
        except:
            st.write('La IA no respondió en el formato esperado. ')
            st.write(response)
        ax.bar([dummy_input], [json.loads(dummy_response)['risk_score']], color='red')
        ax.set_ylim(0, 5)
        ax.set_ylabel('Risk Score')
        ax.set_title('Risk Score Analysis')
        st.pyplot(fig)