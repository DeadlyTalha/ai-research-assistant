import ollama
from retriever import search_document

MODEL_NAME = "qwen3.5:4b"


def generate_response(prompt):
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def build_prompt(question, documents,metadatas):
    
    context_parts = []

    for i in range(len(documents)):
        document = documents[i]
        page = metadatas[i]["page"]

        context_parts.append(
            f"[Page {page}]\n{document}"
        )
    context = "\n\n".join(context_parts)

    prompt = f"""
Tu es un assistant de recherche spécialisé dans l'analyse de documents.

Réponds à la question uniquement à partir du contexte fourni.

Règles :
- N'utilise pas de connaissances extérieures au document.
- Si l'information n'est pas présente dans le contexte, dis clairement :
  "Je ne trouve pas cette information dans le document."
- Donne une réponse claire et concise.
- Lorsque c'est pertinent, indique les pages utilisées.

CONTEXTE DU DOCUMENT :
{context}

QUESTION :

{question}

RÉPONSE :
"""

    return prompt


if __name__ == "__main__":
    question = input("Pose ta question : ")

    # Recherche des chunks pertinents
    results = search_document(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Construire le prompt
    prompt = build_prompt(
        question,
        documents,
        metadatas
    )

    # Générer la réponse
    response = generate_response(prompt)

    print("\n===== RÉPONSE =====")
    print(response)

    print("\n===== SOURCES =====")

    pages = []

    for metadata in metadatas:
        page = metadata["page"]

        if page not in pages:
            pages.append(page)

    for page in pages:
        print(f"- Page {page}")