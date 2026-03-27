from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

messages = []

print("Chat LLaMA 3.1-8B Instant (Ctrl+C pour quitter)\n")

while True:
    try:
        user_input = input("Vous: ")
        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=1
        )

        reply = response.choices[0].message.content
        print(f"Assistant: {reply}\n")

    except KeyboardInterrupt:
        print("\nAu revoir !")
        break