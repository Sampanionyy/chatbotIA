from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"    
)

st.title("Chat LLaMA 3.1-8B Instant avec Streamlit")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.write(f"**{'Vous' if msg['role'] == 'user' else 'Assistant'}:** {msg['content']}")

user_input = st.chat_input("Votre message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages,
        temperature=0
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()