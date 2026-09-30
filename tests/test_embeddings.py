from app.embeddings import create_embeddings


texts = [
    "Employees receive 25 days of annual leave.",
    "How many vacation days do employees get?",
    "The company headquarters is located in London.",
]


embeddings = create_embeddings(texts)

print(f"Number of embeddings: {len(embeddings)}")
print(f"Embedding dimensions: {len(embeddings[0])}")

print("\nFirst embedding:")
print(embeddings[0][:10])