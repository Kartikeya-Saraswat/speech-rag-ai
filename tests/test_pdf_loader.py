from app.loader import extract_text_from_pdf


PDF_PATH = "/Users/kartikeyasaraswat/Desktop/Globtier/speech-rag-ai/data/uploads/Course Material Information - 2022-23 entry - P-C803.pdf"


text = extract_text_from_pdf(PDF_PATH)

print("\n--- EXTRACTED TEXT ---\n")
print(text[:5000])
print("\n--- END ---\n")