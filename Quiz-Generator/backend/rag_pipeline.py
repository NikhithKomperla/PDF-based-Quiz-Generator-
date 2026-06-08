from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from llm import get_mistral_response
import os

def generate_quiz_from_pdf(pdf_path):
    print(f"Processing file: {pdf_path}")
    
    # 1. Load PDF
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages")
    except Exception as e:
        return f"Error loading PDF: {str(e)}"

    # 2. Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks")

   # Use first few chunks directly
context = "\n".join(
    [chunk.page_content for chunk in chunks[:5]]
)
    
    # 6. RAG Prompt
    prompt = f"""
You are an AI quiz generator.
Use ONLY the context below to generate the quiz.

Context:
{context}

Generate 5 multiple-choice questions based on the context above.
Output the result in a STRICT JSON format. Do not add any markdown formatting like ```json ... ``` or any other text. Just the raw JSON list.
The JSON must be a list of objects with this structure:
[
  {{
    "question": "Question text here",
    "options": {{
      "A": "Option A text",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "answer": "Correct Option Key (A, B, C, or D)"
  }}
]
"""

    print("Querying Mistral...")
    return get_mistral_response(prompt)
