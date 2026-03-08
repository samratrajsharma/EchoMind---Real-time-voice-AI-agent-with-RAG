import os
import uvicorn
from dotenv import load_dotenv


def main():
    load_dotenv()

    print("\nSelect model provider:")
    print("1. Ollama (local)")
    print("2. Groq (API)")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        os.environ["MODEL_PROVIDER"] = "ollama"

    elif choice == "2":
        os.environ["MODEL_PROVIDER"] = "groq"

    else:
        print("Invalid choice. Defaulting to Ollama.")
        os.environ["MODEL_PROVIDER"] = "ollama"

    print(f"\nUsing model provider: {os.environ['MODEL_PROVIDER']}\n")

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()