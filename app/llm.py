import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


MODEL_NAME = "openai/gpt-oss-20b"


def generate_answer(
    question: str,
    context: list[str],
) -> str:
    """
    Generate an answer using Groq and retrieved PDF context.
    """

    context_text = "\n\n".join(context)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the document context below.

If the answer cannot be found in the context,
say that the information is not available in the document.

Keep the answer concise and natural.

DOCUMENT CONTEXT:
{context_text}

USER QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content