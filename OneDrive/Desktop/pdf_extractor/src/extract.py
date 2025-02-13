from models.ollama_model import read_single_pdf, chunk_data, create_vector_db, load_vector_db, retrieve_answers
from langchain_ollama import OllamaLLM  # Updated import
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from langchain.llms import Ollama

def extract_data_with_ollama(pdf_path):
    """
    Extract structured data from a document using the Ollama model.
    """
    try:
        # Step 1: Load the PDF
        docs = read_single_pdf(pdf_path)
        
        # Step 2: Split into chunks
        doc_chunks = chunk_data(docs)
        
        # Step 3: Create or load vector database
        db_path = "faiss_index_extraction"
        if not os.path.exists(db_path):
            vector_db = create_vector_db(doc_chunks, db_path)
        else:
            vector_db = load_vector_db(db_path)
        
        # Step 4: Initialize Ollama LLM
        llm = Ollama(model="llama3.2")
        
        # Step 5: Define custom prompt for extraction
        prompt_template = """
        You are an expert assistant tasked with extracting financial data.
        Context: {context}
        Question: {question}
        Please extract and return data in the following JSON format:
        {
            "dates": [],
            "amounts": [],
            "account_codes": [],
            "descriptions": []
        }
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
        
        # Step 7: Retrieve extracted data
        query = "Extract all dates, amounts, account codes, and descriptions from this document."
        extracted_data = retrieve_answers(query, qa_chain)
        return extracted_data

    except Exception as e:
        print(f"Error in extraction: {e}")
        return {
            "dates": [],
            "amounts": [],
            "account_codes": [],
            "descriptions": []
        }