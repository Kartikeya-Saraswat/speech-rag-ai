import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


STT_MODEL = "whisper-large-v3-turbo"


def transcribe_audio(file_path: str) -> str:
    """
    Convert an audio file into text using Groq Whisper.
    """

    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=STT_MODEL,
        )

    return transcription.text