import os
from google import genai

API_KEY = "your_api_key"

client = genai.Client(api_key=API_KEY)

def generate_answer(query, context):
    prompt = f"""
Answer only from the given context.

Context:
{context}

Question:
{query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text
