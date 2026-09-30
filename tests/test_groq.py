from app.llm import generate_answer


question = "What is the main topic of the document?"

context = [
    "This document describes the company's employee benefits "
    "including annual leave, health insurance, and retirement benefits."
]


answer = generate_answer(
    question=question,
    context=context,
)

print("\n--- GROQ RESPONSE ---\n")
print(answer)