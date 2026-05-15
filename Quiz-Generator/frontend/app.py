import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="RAG Quiz Generator",
    page_icon="📘",
    layout="centered"
)

st.title("📘 RAG-Based Quiz Generator (Mistral API)")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF Document", type=["pdf"])

if uploaded_file:
    # Display file details
    st.write(f"Filename: {uploaded_file.name}")
    
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz... This may take a moment."):
            try:
                # Prepare file for upload
                files = {"file": uploaded_file}
                
                # Call backend API
                # Note: Using localhost for now. 
                # If running on different machines, update IP.
                response = requests.post(
                    "http://127.0.0.1:8000/generate-quiz/",
                    files=files
                )

                if response.status_code == 200:
                    data = response.json()
                    quiz_content = data.get("quiz", "")
                    
                    # Store in session state
                    st.session_state["quiz_content"] = quiz_content
                    
                    st.success("Quiz Generated Successfully! Redirecting...")
                    
                    # Redirect to quiz page
                    st.switch_page("pages/quiz.py")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Is it running? (http://127.0.0.1:8000)")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("Powered by Mistral AI & LangChain")
