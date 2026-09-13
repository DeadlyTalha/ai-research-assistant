from embeddings import load_embedding_model
from vector_store import create_vector_store

seuil_distance = 0.9  #seuil de distance pour déterminer la pertinence des résultat

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

    distances = results["distances"][0]

    # Vérifier la pertinence du meilleur résultat
    if distances[0] > seuil_distance: 
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }
    
    return results


if __name__ == "__main__":
    question = input("Pose ta question : ")

    results = search_document(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents:
        print("Pas de chunk pertinent trouvé pour la question posée.")
    else:
        print("\nRésultats trouvés :")
        
        for i in range(len(documents)):
            document = documents[i]
            page = metadatas[i]["page"]
            distance = distances[i]

            print(f"\n--- Résultat {i + 1} | Page {page}  ---")
            print(f"Distance : {distance:.4f}") #affiche le score de similarité
            print(document[:500])