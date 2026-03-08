import ollama
from groq import Groq

from backend.config import (
    MODEL_PROVIDER,
    OLLAMA_MODEL
)

groq_client = Groq()


def generate_answer(prompt: str):
    """
    Route the prompt to the selected LLM provider.
    Change provider from .env using MODEL_PROVIDER.
    """

    if MODEL_PROVIDER == "ollama":

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]

    elif MODEL_PROVIDER == "groq":

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    else:
        raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")