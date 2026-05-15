import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

def get_mistral_response(prompt: str):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set properly in .env file")
        
    client = Mistral(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages
    )

    return response.choices[0].message.content
