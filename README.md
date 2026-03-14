# EchoMind --- AI Voice Knowledge Assistant

EchoMind is a **modern AI Voice Knowledge Assistant powered by
Retrieval-Augmented Generation (RAG)**.

It allows users to:

-   Upload documents
-   Ask questions using **voice**
-   Retrieve **context-aware answers**
-   View **AI reasoning traces**
-   See **sources used for the answer**
-   Monitor **system latency**

The system combines **vector search, hybrid retrieval, streaming LLM
responses, and a modern UI** to create an interactive AI knowledge
assistant.

EchoMind demonstrates how to build a **production-style AI application
from scratch** integrating backend AI pipelines with a modern frontend.

------------------------------------------------------------------------

# 🚀 Key Features

## 🎤 Voice Interaction

Speak naturally using your microphone. EchoMind converts speech into
text queries using browser speech recognition.

## 📄 Document Knowledge Base

Upload documents that are automatically:

-   Parsed
-   Chunked
-   Embedded
-   Stored in a vector database

## 🧠 Retrieval Augmented Generation (RAG)

EchoMind retrieves relevant document chunks and feeds them into the LLM
so answers are **grounded in real data instead of hallucinated
responses**.

## ⚡ Streaming AI Responses

Answers stream token-by-token from the LLM similar to ChatGPT.

## 🔎 Hybrid Retrieval

EchoMind combines:

-   **Vector Search**
-   **BM25 Keyword Search**

This significantly improves retrieval accuracy.

## 📊 AI Insight Panels

EchoMind exposes internal AI pipeline signals including:

-   Sources used
-   Latency metrics
-   Agent reasoning trace

## 🔊 Voice Output

AI responses are spoken back to the user using browser speech synthesis.

## 🧠 Conversation Memory

Conversation history is maintained to support contextual dialogue.

------------------------------------------------------------------------

# 🧠 System Architecture

    Browser Microphone
            │
            ▼
    SpeechRecognition API
            │
            ▼
    React Frontend
            │
            ▼
    FastAPI Backend
            │
            ▼
    Hybrid RAG Retrieval
    (Vector Search + BM25)
            │
            ▼
    Large Language Model
    (Groq API / Ollama Local)
            │
            ▼
    Streaming Response
            │
            ▼
    Frontend UI + Voice Output

------------------------------------------------------------------------

# 🛠 Technologies Used

## Backend

-   Python
-   FastAPI
-   SentenceTransformers
-   Qdrant Vector Database
-   BM25 (rank_bm25)
-   Groq API
-   Ollama (Local LLM)
-   Streaming LLM inference

## Frontend

-   React
-   Vite
-   Modern CSS UI
-   Web Speech API
-   Speech Synthesis API

## AI Infrastructure

-   Retrieval Augmented Generation (RAG)
-   Hybrid Retrieval
-   Vector Embeddings
-   Streaming token generation
-   Source attribution
-   Latency monitoring

------------------------------------------------------------------------

# 📁 Project Structure

    EchoMind
    │
    ├── backend
    │   │
    │   ├── config.py
    │   ├── main.py
    │   │
    │   ├── rag
    │   │   ├── ingest.py
    │   │   ├── retriever.py
    │   │   └── document_loader.py
    │   │
    │   ├── services
    │   │   ├── embedding_service.py
    │   │   ├── llm_service.py
    │   │   └── memory.py
    │   │
    │   └── vector_db
    │       └── qdrant_client.py
    │
    ├── frontend
    │   │
    │   ├── src
    │   │   ├── components
    │   │   │   └── VoiceRoom_1.jsx
    │   │   │
    │   │   ├── App.jsx
    │   │   ├── index.css
    │   │   └── main.jsx
    │   │
    │   └── package.json
    │
    ├── data
    │   └── outputs
    │
    ├── run.py
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

# 📦 Installation

Clone the repository:

``` bash
git clone https://github.com/yourusername/EchoMind.git
cd EchoMind
```

Create Python environment:

``` bash
conda create -n echomind python=3.10
conda activate echomind
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# 🔑 Environment Variables

Create a `.env` file in the root directory.

    GROQ_API_KEY=your_groq_api_key

    MODEL_PROVIDER=groq

    OLLAMA_MODEL=llama3:8b

------------------------------------------------------------------------

# ▶ Running the Application

## Start Backend

    python run.py

Backend runs at:

    http://127.0.0.1:8000

------------------------------------------------------------------------

## Start Frontend

    cd frontend
    npm install
    npm run dev

Frontend runs at:

    http://localhost:5173

------------------------------------------------------------------------

# 🧪 Usage

1️⃣ Upload a document\
2️⃣ Click **Speak**\
3️⃣ Ask a question about the document

Example:

    What is the company name mentioned in the document?

EchoMind will:

1.  Retrieve relevant document chunks
2.  Generate an answer using the LLM
3.  Stream the response
4.  Display citations and system metrics

------------------------------------------------------------------------

# 📊 AI Insight Panels

## Sources Used

Displays which document chunks were used by the model.

Example:

    invoice.pdf (chunk 2)
    invoice.pdf (chunk 5)

------------------------------------------------------------------------

## Latency Metrics

    RAG Retrieval: 120 ms

------------------------------------------------------------------------

## Agent Trace

    User query received
    Retrieving documents
    Retrieved 3 chunks
    Generating answer

------------------------------------------------------------------------

# 🖼 Screenshots

## Model Selection

![Model Choice](outputs_images/Model_Choice.png)

## Document Upload

![Document Upload](outputs_images/Document_Upload.png)

## Results using Groq API

![Groq Results](outputs_images/Results_Fetched_Groq_API.png)

## Results using Ollama

![Ollama Results](outputs_images/Results_Fetched_Ollama.png)

## AI Output

![AI Output](outputs_images/Al_Output.png)

## Updated AI Output

![AI Output Updated](outputs_images/Al_Output_Updated_Ul.png)

## Retrieved Details

![Details](outputs_images/Details_Fetched.png)

------------------------------------------------------------------------

# 🎯 Why EchoMind is Interesting

EchoMind demonstrates how to build a **real AI system** combining:

-   Voice interfaces
-   Retrieval augmented generation
-   Hybrid search
-   Streaming LLM responses
-   Vector databases
-   Explainable AI outputs

The project integrates **machine learning, backend engineering, and
frontend UX** into a cohesive AI product.

------------------------------------------------------------------------

# 📈 Future Improvements

Possible extensions:

-   multi-document knowledge bases
-   semantic caching
-   long-term memory
-   multi-modal document support
-   cloud deployment
-   authentication

------------------------------------------------------------------------

# 🧑‍💻 Author

**Samrat Raj Sharma**

AI / ML Engineer

EchoMind was built to explore the intersection of:

-   Voice interfaces
-   Retrieval-Augmented Generation
-   Modern AI system design

------------------------------------------------------------------------

# ⭐ If you like this project

Consider **starring the repository** and sharing it with others
interested in building AI systems.
