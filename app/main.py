from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import answer_question


app = FastAPI(
    title="Speech RAG AI",
    description="Conversational AI with PDF-based RAG",
    version="0.1.0",
)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    answer = answer_question(request.question)

    return {
        "answer": answer
    }