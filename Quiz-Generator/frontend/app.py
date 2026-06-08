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
    st.write(f"Filename: {uploaded_file.name}")

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz... This may take a moment."):
            try:
                files = {"file": uploaded_file}

                # Render Backend URL
                response = requests.post(
                    "https://pdf-based-quiz-generator.onrender.com/generate-quiz/",
                    files=files,
                    timeout=120
                )

                if response.status_code == 200:
                    data = response.json()
                    quiz_content = data.get("quiz", "")

                    st.session_state["quiz_content"] = quiz_content

                    st.success("Quiz Generated Successfully!")

                    st.switch_page("pages/quiz.py")

                else:
                    st.error(
                        f"Backend Error: {response.status_code}\n\n{response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the Render backend."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "Request timed out. Try again with a smaller PDF."
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("Powered by Mistral AI & LangChain")
