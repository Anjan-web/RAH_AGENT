import os
from groq import Groq
from dotenv import load_dotenv

# Load env ONCE (safe locally, ignored on Streamlit Cloud)
load_dotenv()

# Create client ONCE
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt: str) -> str:
    """
    Ask Groq LLM.
    Safe for Streamlit & deployment.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b"
,
        messages=[
            {
                "role": "system",
                "content": "You are a senior cybersecurity analyst. Be precise and practical."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()
