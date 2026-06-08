import streamlit as st
import requests

st.set_page_config(
    page_title="RAG Quiz Generator",
    page_icon="📘",
    layout="centered"
)

st.title("📘 RAG-Based Quiz Generator (Mistral API)")

uploaded_file = st.file_uploader(
    "Upload a PDF Document",
    type=["pdf"]
)

if uploaded_file:
    st.write(f"Filename: {uploaded_file.name}")

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz..."):
            try:
                files = {"file": uploaded_file}

                response = requests.post(
                    "https://pdf-based-quiz-generator.onrender.com/generate-quiz/",
                    files=files,
                    timeout=120
                )

                if response.status_code == 200:
                    data = response.json()

                    st.session_state["quiz_content"] = data.get("quiz", "")

                    st.success("Quiz Generated Successfully!")

                    st.switch_page("pages/quiz.py")

                else:
                    st.error(
                        f"Backend Error {response.status_code}: {response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to Render backend.")

            except requests.exceptions.Timeout:
                st.error("Request timed out.")

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("Powered by Mistral AI & LangChain")
