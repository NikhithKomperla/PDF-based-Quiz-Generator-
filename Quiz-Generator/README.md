# RAG Quiz Generator

A RAG-based Quiz Generator using FastAPI, Streamlit, and Mistral AI.

## Project Structure
- `backend/`: FastAPI server for processing PDFs and generating quizzes.
- `frontend/`: Streamlit dashboard for uploading documents and taking quizzes.

## How to Run

### 1. Start the Backend
Open a terminal and run:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
The backend will be running at `http://127.0.0.1:8000`.

### 2. Start the Frontend
Open a **new** terminal and run:
```powershell
cd frontend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
The frontend will be running at `http://127.0.0.1:8501`.

## Prerequisites
- Python 3.8+
- Mistral API Key (configured in `backend/.env`)
