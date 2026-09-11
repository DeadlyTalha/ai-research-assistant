from embeddings import load_embedding_model
from vector_store import create_vector_store


def search_document(question, top_k=3):
    
    collection = create_vector_store()

    # générer l'embedding de la question
    model = load_embedding_model()
    question_embedding = model.encode([question])

       # rechercher les chunks les plus pertinents
    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=top_k
    )

    return results


if __name__ == "__main__":
    question = input("Pose ta question : ")

    results = search_document(question)

    print("\nRésultats trouvés :")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i in range(len(documents)):
        document = documents[i]
        page = metadatas[i]["page"]

        print(f"\n--- Résultat {i + 1} | Page {page} ---")
        print(document[:1000])