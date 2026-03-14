import ollama
from groq import Groq

from backend.config import (
    MODEL_PROVIDER,
    OLLAMA_MODEL,
    GROQ_MODEL
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
    

def stream_generated_answer(prompt: str):
    if MODEL_PROVIDER == 'ollama':
        stream = ollama.chat(
            model = OLLAMA_MODEL,
            messages = [{'role': 'user', 'content':prompt}],
            stream = True
        )

        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['messages']:
                yield chunk['messages']['content']

    elif MODEL_PROVIDER == 'groq':
        stream = groq_client.chat.completions.create(
            model = GROQ_MODEL,
            messages = [{'role': 'user', 'content':prompt}],
            stream = True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    else:
        raise ValueError('Unsupported MODEL_PROVIDER')