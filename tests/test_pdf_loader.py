from app.loader import extract_text_from_pdf
from app.chunker import chunk_text


PDF_PATH = "/Users/kartikeyasaraswat/Desktop/Globtier/speech-rag-ai/data/uploads/Course Material Information - 2022-23 entry - P-C803.pdf"


text = extract_text_from_pdf(PDF_PATH)

chunks = chunk_text(text)

print(f"\nTotal characters: {len(text)}")
print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- CHUNK {i + 1} ---\n")
    print(chunk)