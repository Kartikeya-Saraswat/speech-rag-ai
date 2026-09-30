from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.rag import answer_question
from app.ingestion import ingest_pdf


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

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"data/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    chunks_created = ingest_pdf(file_path)

    return {
        "filename": file.filename,
        "chunks_created": chunks_created,
        "status": "processed",
    }

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    answer = answer_question(request.question)

    return {
        "answer": answer
    }