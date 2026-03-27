from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Check if the API key is set in .env file
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")
print(f"GROQ_API_KEY: {api_key}")

# Create GROQ client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

print("GROQ client created successfully")

# Send the request
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)
print(f"Response: {response.choices[0].message.content}")
st.write(f"Response: {response.choices[0].message.content}")

