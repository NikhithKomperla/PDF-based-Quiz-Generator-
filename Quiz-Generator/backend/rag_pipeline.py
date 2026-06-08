from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm import get_mistral_response

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

    # 3. Use chunks directly (No FAISS, No Embeddings)
    print("Preparing context...")

    context = "\n".join(
        [chunk.page_content for chunk in chunks[:10]]
    )

    # 4. Prompt
    prompt = f"""
You are an AI quiz generator.

Use ONLY the context below to generate the quiz.

Context:
{context}

Generate 5 multiple-choice questions based on the context above.

Output the result in STRICT JSON format.

Do not add markdown formatting.
Do not add explanations.
Return only a raw JSON list.

The JSON structure must be:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "A"
  }}
]
"""

    print("Querying Mistral...")
    return get_mistral_response(prompt)
