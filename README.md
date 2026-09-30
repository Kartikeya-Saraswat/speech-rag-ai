# Speech RAG AI

A lightweight **Speech-to-Speech Conversational AI** application that
answers questions from uploaded PDF documents.

The system combines: - **FastAPI** for the backend API - **Groq
Whisper** for speech-to-text - **Local Sentence Transformers** for
embeddings - **ChromaDB** for vector retrieval - **Groq GPT-OSS 20B**
for answer generation - **Groq Orpheus TTS** for text-to-speech - A
simple browser frontend for PDF upload and microphone interaction

## Architecture

``` text
                         ┌──────────────────────┐
                         │      Browser UI       │
                         │                      │
                         │  PDF Upload + Mic    │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         └───────┬───────┬──────┘
                                 │       │
                    PDF Upload   │       │ Voice Question
                                 │       │
                    ┌────────────▼─┐   ┌─▼──────────────┐
                    │ PDF Ingestion│   │  Groq Whisper  │
                    │              │   │     STT        │
                    │ PyMuPDF      │   └───────┬────────┘
                    │ Chunking     │           │
                    │ Embeddings   │           ▼
                    └──────┬───────┘      Question Text
                           │                    │
                           ▼                    ▼
                    ┌──────────────┐     ┌──────────────┐
                    │   ChromaDB   │◄────│   Embedding  │
                    │ Vector Store │     │    Query     │
                    └──────┬───────┘     └──────┬───────┘
                           │                    │
                           └──────────┬─────────┘
                                      ▼
                              ┌──────────────┐
                              │  Groq LLM    │
                              │ GPT-OSS 20B  │
                              └──────┬───────┘
                                     │
                                  Answer
                                     │
                                     ▼
                              ┌──────────────┐
                              │ Groq Orpheus │
                              │     TTS      │
                              └──────┬───────┘
                                     │
                                     ▼
                               Browser Audio
```

## Project Structure

``` text
speech-rag-ai/
├── app/
│   ├── main.py          # FastAPI application and API endpoints
│   ├── loader.py        # PDF text extraction
│   ├── chunker.py       # Text chunking
│   ├── embeddings.py    # Local Sentence Transformer embeddings
│   ├── vector_store.py  # ChromaDB storage and retrieval
│   ├── llm.py           # Groq LLM integration
│   ├── rag.py           # Retrieval-Augmented Generation pipeline
│   ├── ingestion.py     # End-to-end PDF ingestion
│   ├── speech.py        # Groq Whisper speech-to-text
│   └── tts.py           # Groq Orpheus text-to-speech
├── frontend/
│   └── index.html       # Browser UI
├── data/
│   ├── uploads/         # Uploaded PDFs (ignored by Git)
│   └── chroma/          # Persistent ChromaDB data (ignored by Git)
├── tests/               # Component/API tests
├── .env                 # API key configuration (ignored)
├── .env.example         # Environment variable template
├── requirements.txt
└── README.md
```

## Prerequisites

-   Python 3.12+
-   A Groq API key
-   macOS/Linux/Windows
-   Microphone for voice interaction

## Setup

### 1. Clone the repository

``` bash
git clone <repository-url>
cd speech-rag-ai
```

### 2. Create virtual environment

``` bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Groq

Create `.env`:

``` env
GROQ_API_KEY=your_groq_api_key
```

Never commit `.env`.

### 5. Start the application

Use the project Python interpreter:

``` bash
python -m uvicorn app.main:app --reload
```

Open:

``` text
http://127.0.0.1:8000
```

FastAPI documentation:

``` text
http://127.0.0.1:8000/docs
```

## How to Use

### Step 1 --- Upload a PDF

Select a PDF and click **Upload PDF**.

The ingestion pipeline:

``` text
PDF
 ↓
PyMuPDF text extraction
 ↓
Character-based chunking
 ↓
Sentence Transformer embeddings
 ↓
ChromaDB
```

### Step 2 --- Ask a question

Click **Start Recording**, speak your question, then click **Stop
Recording**.

The voice pipeline:

``` text
Microphone
 ↓
Groq Whisper
 ↓
Question text
 ↓
Embedding
 ↓
ChromaDB similarity search
 ↓
Top relevant chunks
 ↓
Groq LLM
 ↓
Answer
 ↓
Groq Orpheus TTS
 ↓
Audio response
```

## API Endpoints

  Endpoint    Method   Purpose
  ----------- -------- -------------------------
  `/`         GET      Browser frontend
  `/health`   GET      Health check
  `/upload`   POST     Upload and index PDF
  `/ask`      POST     Text-based RAG question
  `/voice`    POST     Speech → RAG → speech

## RAG Design

The application uses a simple retrieval-augmented generation flow.

1.  Extract text from the PDF.
2.  Split text into overlapping chunks.
3.  Generate local vector embeddings.
4.  Store chunks and embeddings in ChromaDB.
5.  Convert the user's question into an embedding.
6.  Retrieve the top 3 similar chunks.
7.  Pass the retrieved context to the Groq LLM.
8.  Instruct the LLM to answer only from the supplied document context.

This reduces dependence on model-only knowledge and grounds the response
in the uploaded document.

## Key Technology Choices

### Groq

Used for: - Speech-to-text - LLM inference - Text-to-speech

This provides a single inference provider for the cloud AI components.

### Sentence Transformers

`all-MiniLM-L6-v2` is used locally for embeddings.

Advantages: - No embedding API cost - Fast enough for a small
prototype - 384-dimensional embeddings - Simple local deployment

### ChromaDB

Used as the vector database.

It stores: - document chunks - embeddings - document metadata - chunk
indexes

### FastAPI

Provides a lightweight backend and exposes both REST APIs and the
browser application.

## Current MVP Scope

Implemented:

-   PDF upload
-   PDF text extraction
-   Text chunking
-   Local embeddings
-   Persistent vector store
-   Semantic retrieval
-   Groq LLM generation
-   Speech-to-text
-   Text-to-speech
-   End-to-end speech-to-speech interaction
-   Browser microphone interface
-   Basic document metadata
-   API documentation through Swagger

## Known MVP Limitations

-   Retrieval currently searches the shared Chroma collection rather
    than explicitly filtering to one selected document.
-   Chunking is character-based rather than semantic/structure-aware.
-   Conversation history is not persisted.
-   TTS responses should remain short because the selected Orpheus model
    has an input-length limitation.
-   Authentication and production security are not implemented.
-   ChromaDB is local and intended for the prototype.
-   Browser audio formats can vary by browser.

## Future Improvements

1.  Add document-specific retrieval filters.
2.  Add conversation memory.
3.  Improve chunking using headings/paragraph boundaries.
4.  Add citations showing the source PDF and page number.
5.  Stream LLM/TTS responses for lower perceived latency.
6.  Add authentication and rate limiting.
7.  Containerize the application.
8.  Move vector storage to a production vector database if required.
9.  Add automated tests and CI/CD.
10. Add observability for latency, retrieval quality, and API failures.

## Demo Question

For the Warwick course PDF used during development:

> How will students be assessed at Warwick?

Example grounded response:

> Students at Warwick are assessed through a mix of methods, including
> worksheets, essays, research reports, modelling and data analysis,
> class tests, exams, and presentations.

## Git Checkpoints

The project was developed incrementally using feature-focused commits:

``` text
chore: initialize speech rag application
chore: add initial application dependencies
feat: add pdf text extraction
feat: add document chunking
feat: add local text embeddings
feat: add groq llm integration
feat: add vector retrieval with chromadb
feat: add end-to-end rag pipeline
feat: expose rag pipeline through fastapi
feat: add pdf upload and ingestion api
feat: add document metadata to vector store
feat: add groq text to speech
feat: add speech to speech rag endpoint
feat: add browser speech rag interface
```
