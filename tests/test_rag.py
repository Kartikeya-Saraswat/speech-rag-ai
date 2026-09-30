from app.rag import answer_question


question = "How will students be assessed at Warwick?"

answer = answer_question(question)

print("\n--- RAG ANSWER ---\n")
print(answer)