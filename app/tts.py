import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


TTS_MODEL = "canopylabs/orpheus-v1-english"


def synthesize_speech(
    text: str,
    output_path: str,
) -> str:
    """
    Convert text into speech using Groq TTS.
    """

    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice="autumn",
        input=text,
        response_format="wav",
    )

    response.write_to_file(output_path)

    return output_path