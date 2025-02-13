import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
import time
import sys

load_dotenv()

def list_pdf_files(directory):
    """List all PDF files in the specified directory."""
    pdf_files = [f for f in os.listdir(directory) if f.endswith('sample.pdf')]
    return pdf_files

def read_single_pdf(file_path):
    print(f"Loading PDF from path: {file_path}")  # Debug statement
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def chunk_data(docs, chunk_size=1000, chunk_overlap=100):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc_chunks = text_splitter.split_documents(docs)
    return doc_chunks

def create_vector_db(documents, db_path):
    """Create a FAISS vector database."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.from_documents(documents, embeddings)
    vector_db.save_local(db_path)
    print(f"Vector database saved at {db_path}")
    return vector_db

def load_vector_db(db_path):
    """Load an existing FAISS vector database."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    print(f"Vector database loaded from {db_path}")
    return vector_db

def retrieve_answers(query, qa_chain):
    """
    Retrieve answers using the QA chain.
    """
    try:
        # Use invoke instead of run
        response = qa_chain.invoke({"query": query})
        # Extract the answer from the response
        if isinstance(response, dict):
            return response.get("result", "")
        return str(response)
    except Exception as e:
        print(f"Error retrieving answer: {e}")
        return ""

def initialize_qa_chain(vector_db, prompt_template):
    """Initialize a RetrievalQA chain."""
    llm = Ollama(model="llama3.2")
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain
def initialize_qa_chain(vector_db, prompt_template):
    """
    Initialize a RetrievalQA chain with the given vector database and prompt template.
    """
    llm = Ollama(model="llama3.2")
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

def classify_document(vector_db, query="Classify this document."):
    """
    Classify a document using the Ollama model.
    """
    prompt_template = """
    You are an expert assistant tasked with classifying documents.
    Context: {context}
    Question: What type of document is this? (e.g., invoice, receipt, ledger)
    Answer:
    """
    qa_chain = initialize_qa_chain(vector_db, prompt_template)
    classification = retrieve_answers(query, qa_chain)
    return classification.strip()

def extract_data(vector_db, query="Extract financial data."):
    """
    Extract structured data from a document using the Ollama model.
    """
    prompt_template = """
    You are an expert assistant tasked with extracting financial data.
    Context: {context}
    Question: Extract key fields such as dates, amounts, account codes, and descriptions.
    Answer:
    """
    qa_chain = initialize_qa_chain(vector_db, prompt_template)
    extracted_data = retrieve_answers(query, qa_chain)
    return extracted_data.strip()