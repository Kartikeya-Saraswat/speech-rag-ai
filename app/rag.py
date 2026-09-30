from app.embeddings import create_embeddings
from app.vector_store import search
from app.llm import generate_answer


def answer_question(question: str) -> str:
    """
    Retrieve relevant PDF context and generate an answer.
    """

    query_embedding = create_embeddings([question])[0]

    relevant_chunks = search(
        query_embedding,
        top_k=3,
    )

    answer = generate_answer(
        question=question,
        context=relevant_chunks,
    )

    return answer