import os
import tempfile

from app.ingestion import ingest_pdf
from app.rag import answer_question
from app.speech import transcribe_audio
from app.tts import synthesize_speech
from app.ingestion import ingest_pdf
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI(
    title="Speech RAG AI",
    description="Conversational AI with PDF-based RAG",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def frontend():
    return FileResponse("frontend/index.html")


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

    document_id, chunks_created = ingest_pdf(
        file_path=file_path, 
        filename=file.filename,
    )

    return {
        "filename": file.filename,
        "chunks_created": chunks_created,
        "document_id": document_id,
        "status": "processed",
    }

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    answer = answer_question(request.question)

    return {
        "answer": answer
    }

@app.post("/voice")
async def voice_question(file: UploadFile = File(...)):
    """
    Accept an audio question and return a spoken RAG answer.
    """

    with tempfile.TemporaryDirectory() as temp_dir:

        # 1. Save incoming audio
        input_path = os.path.join(
            temp_dir,
            "input.wav",
        )

        with open(input_path, "wb") as buffer:
            buffer.write(await file.read())

        # 2. Speech → Text
        question = transcribe_audio(input_path)

        # 3. RAG → Answer
        answer = answer_question(question)

        # 4. Text → Speech
        output_path = os.path.join(
            temp_dir,
            "response.wav",
        )

        synthesize_speech(
            text=answer,
            output_path=output_path,
        )

        # 5. Read audio before temporary directory is deleted
        with open(output_path, "rb") as audio_file:
            audio_data = audio_file.read()

    # 6. Return audio bytes
    return Response(
        content=audio_data,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'attachment; filename="response.wav"',
        },
    )