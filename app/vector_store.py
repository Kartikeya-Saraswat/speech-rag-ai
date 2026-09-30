import chromadb


CHROMA_PATH = "data/chroma"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="pdf_documents"
)


def add_documents(
    documents: list[str],
    embeddings: list[list[float]],
) -> None:
    """
    Store document chunks and their embeddings in ChromaDB.
    """

    ids = [f"chunk_{i}" for i in range(len(documents))]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
    )


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