import os
import logging
import numpy as np
from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

logging.basicConfig(level=logging.INFO)

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
    return """You are a cybersecurity risk analyst.
    You are tasked with analyzing the risks of the laboratory's infrastructure.
    Analyze the risks of the laboratory's infrastructure and score the risks from 1 to 5, 
    Where 1 is the lowest risk and 5 is the highest risk.
    Given the following context from a nist cibersecurity framweork, assess the risk.
    
    {context}

    The output should be only in this format and no other format is accepted:
    {{
        "risk_score": 3,
        "risk_description": "The laboratory's network traffic is not encrypted.",
        "risk_mitigation": "Encrypt the laboratory's network traffic.",
        "risk_impact": "If the laboratory's network traffic is not encrypted, sensitive data can be intercepted."
    }}
    """

def analyze_row(llm, row, rag_chain):
    """Uses the language model to analyze a row of network traffic data."""
    # template = get_template()
    # input_data = f"Network traffic log: {row[1]}"
    # prompt = template.replace("Input:", input_data)

    input_data = row[1]
    
    # response = llm.invoke(prompt)
    response = rag_chain.invoke({"input": input_data})

    return response


def create_vector_store():
    """Creates an embedding for the NIST document or loads it from a file if it already exists."""
    file_path = "nist.pdf"
    embeddings_cache_file = "embeddings.npy"  # File to save embeddings
    metadata_cache_file = "metadata.npy"  # File to save metadata
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    if os.path.exists(embeddings_cache_file) and os.path.exists(metadata_cache_file):
        logging.info("Loading vector store from cache.")
        # Load embeddings and metadata from files
        vectors = np.load(embeddings_cache_file, allow_pickle=True).tolist()
        metadata = np.load(metadata_cache_file, allow_pickle=True).tolist()
        
        # Create vector store from loaded data
        vectorstore = InMemoryVectorStore.from_documents(splits, OpenAIEmbeddings(), metadata=metadata)
    else:
        logging.info("Creating a new vector store.")


        # Create embeddings
        embeddings = OpenAIEmbeddings()
        texts = [doc.page_content for doc in splits]  # Extract text content from Document objects
        vectors = embeddings.embed_documents(texts)  # Compute embeddings
        metadata = [doc.metadata for doc in splits]  # Collect metadata

        # Create and save the vector store
        vectorstore = InMemoryVectorStore.from_documents(
            documents=splits,  # Use Document objects directly
            embedding=embeddings
        )

        # Save embeddings and metadata to files for future use
        np.save(embeddings_cache_file, np.array(vectors, dtype=object))
        np.save(metadata_cache_file, np.array(metadata, dtype=object))
        logging.info("Vector store created and saved to cache.")

    retriever = vectorstore.as_retriever()
    return retriever

def create_rag_chain(llm):
    """Creates a RAG chain for analyzing data."""
    # Define the prompt template
    prompt_template = get_template()
    
    # Create a prompt object with the variable name 'document'
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_template),
            ("human", "{input}"),
        ]
    )

    retriever = create_vector_store()

    # Now create the QA chain with the prompt
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    logging.info("RAG chain created successfully.")
    return rag_chain

def main():

    # Example row of network traffic data
    row = [1, "Network scanning activity detected from 192.168.1.101 on multiple ports", "sede 1", "2024-10-17"]

    llm = initialize_llm()
    
    rag_chain = create_rag_chain(llm)

    response = analyze_row(llm, row, rag_chain)

    print(response["answer"])

if __name__ == "__main__":
    main()
