from app.loader import extract_text_from_pdf
from app.chunker import chunk_text
from app.embeddings import create_embeddings
from app.vector_store import add_documents, search


PDF_PATH = "/Users/kartikeyasaraswat/Desktop/Globtier/speech-rag-ai/data/uploads/Course Material Information - 2022-23 entry - P-C803.pdf"


# 1. Extract text
text = extract_text_from_pdf(PDF_PATH)


# 2. Split into chunks
chunks = chunk_text(text)


# 3. Create embeddings
embeddings = create_embeddings(chunks)


# 4. Store chunks + embeddings
add_documents(chunks, embeddings)


# 5. Search
question = "What is this document mainly about?"

query_embedding = create_embeddings([question])[0]

results = search(query_embedding, top_k=3)


print("\n--- RETRIEVED CHUNKS ---")

for i, result in enumerate(results):
    print(f"\n### Result {i + 1}\n")
    print(result[:1000])