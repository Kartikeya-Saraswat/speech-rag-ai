import uuid

import chromadb


CHROMA_PATH = "data/chroma"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="pdf_documents"
)


def add_documents(
    documents: list[str],
    embeddings: list[list[float]],
    filename: str,
) -> str:
    """
    Store document chunks, embeddings, and metadata in ChromaDB.

    Returns:
        A unique document ID.
    """

    document_id = str(uuid.uuid4())

    ids = [
        f"{document_id}_{i}"
        for i in range(len(documents))
    ]

    metadatas = [
        {
            "filename": filename,
            "document_id": document_id,
            "chunk_index": i,
        }
        for i in range(len(documents))
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return document_id


def search(
    query_embedding: list[float],
    top_k: int = 3,
) -> list[str]:
    """
    Retrieve the most relevant document chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results["documents"][0]