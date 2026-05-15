from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from rag_pipeline import generate_quiz_from_pdf

app = FastAPI(title="RAG Quiz Generator (Mistral)")

@app.post("/generate-quiz/")
async def generate_quiz(file: UploadFile = File(...)):
    try:
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        file_path = f"temp/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        quiz = generate_quiz_from_pdf(file_path)
        
        # Cleanup (optional, keeping for debugging for now)
        # os.remove(file_path)

        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "RAG Quiz Generator API is running!"}
