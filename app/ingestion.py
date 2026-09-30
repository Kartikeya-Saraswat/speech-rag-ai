from app.loader import extract_text_from_pdf
from app.chunker import chunk_text
from app.embeddings import create_embeddings
from app.vector_store import add_documents


def ingest_pdf(file_path: str) -> int:
    """
    Process a PDF and store its chunks in ChromaDB.

    Returns:
        Number of chunks stored.
    """

    # 1. Extract text
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        raise ValueError("No text could be extracted from the PDF.")

    # 2. Split text into chunks
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError("No chunks were created from the PDF.")

    # 3. Create embeddings
    embeddings = create_embeddings(chunks)

    # 4. Store chunks and embeddings
    add_documents(
        documents=chunks,
        embeddings=embeddings,
    )

    return len(chunks)