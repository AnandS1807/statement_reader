# src/classify.py
import os
from models.ollama_model import read_single_pdf, chunk_data, create_vector_db, load_vector_db, retrieve_answers
from langchain_ollama import OllamaLLM 
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
def classify_document_with_ollama(pdf_path):
    """
    Classify a document using the Ollama model.
    """
    try:
        # Step 1: Load the PDF
        docs = read_single_pdf(pdf_path)
        
        # Step 2: Split into chunks
        doc_chunks = chunk_data(docs)
        
        # Step 3: Create or load vector database
        db_path = "faiss_index_classification"
        if not os.path.exists(db_path):
            vector_db = create_vector_db(doc_chunks, db_path)
        else:
            vector_db = load_vector_db(db_path)
        
        # Step 4: Initialize Ollama LLM
        llm = Ollama(model="llama3.2")
        
        # Step 5: Define custom prompt for classification
        prompt_template = """
        You are an expert assistant tasked with classifying documents.
        Context: {context}
        Question: {question}
        Please classify this document as one of: invoice, receipt, ledger, statement, or other.
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Step 6: Initialize RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(),
            chain_type_kwargs={
                "prompt": PROMPT,
                "verbose": True
            }
        )
        
        # Step 7: Retrieve classification
        query = "What type of document is this?"
        classification = retrieve_answers(query, qa_chain)
        return classification.strip()

    except Exception as e:
        print(f"Error in classification: {e}")
        return "unknown"