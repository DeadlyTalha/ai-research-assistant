from embeddings import load_embedding_model
from vector_store import create_vector_store
from reranker import rerank_documents
from query_classifier import classify_question


#DISTANCE_THRESHOLD = 1.2
RERANK_THRESHOLD = -3.0

RETRIEVAL_TOP_K = 50
FINAL_TOP_K = 5

def get_global_context(collection, num_chunks=8):
    all_data = collection.get(
        include=["documents", "metadatas"]
    )

    documents = all_data["documents"]
    metadatas = all_data["metadatas"]

    if not documents:
        return [], []

    # Trier les chunks selon leur page
    chunks = sorted(
        zip(documents, metadatas),
        key=lambda x: x[1]["page"]
    )

    # Sélectionner des chunks répartis dans tout le document
    step = max(1, len(chunks) // num_chunks)

    selected = chunks[::step][:num_chunks]

    selected_documents = [item[0] for item in selected]
    selected_metadatas = [item[1] for item in selected]

    return selected_documents, selected_metadatas



def search_document(question):
    """
    Recherche les chunks pertinents en deux étapes :

    1. Retrieval avec ChromaDB
    2. Reranking avec un CrossEncoder
    """
    
    collection = create_vector_store()
    question_type = classify_question(question)

    print(f"\nType de question : {question_type}")

    if question_type == "GLOBAL":

        documents, metadatas = get_global_context(
            collection,
            num_chunks=8
        )

        return {
            "documents": [documents],
            "metadatas": [metadatas],
            "distances": [[]],
            "rerank_scores": [[]]
        }
    
    
    
    """data = collection.get()

    print("\n===== VÉRIFICATION INDEX =====")

    for i, metadata in enumerate(data["metadatas"]):
        if metadata["page"] == 13:
            print("CHUNK PAGE 13 TROUVÉ !")
            print(data["documents"][i][:1000]) """
    
    embedding_model = load_embedding_model()

    # Retrieval avec ChromaDB

    question_embedding = embedding_model.encode([question])

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=RETRIEVAL_TOP_K
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Aucun résultat
    if not documents:
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "rerank_scores": [[]]
        }

    # Seuil de distance pour filtrer les résultats peu pertinents
    print("\n===== RÉSULTATS CHROMA =====")

    for i in range(len(documents)):
        print(f"\n--- Résultat {i+1} ---")
        print(f"Page : {metadatas[i]['page']}")
        print(f"Distance : {distances[i]}")
        print(f"Texte : {documents[i][:300]}")
    
    """if distances[0] > DISTANCE_THRESHOLD:
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "rerank_scores": [[]]
        }"""

   # Reranking

    ranked_documents = rerank_documents(
        question,
        documents,
        top_k=FINAL_TOP_K
    )

    print("\n===== DEBUG RERANKER =====")

    for result in ranked_documents:
        print(
            f"Index : {result['index']} | "
            f"Score : {result['score']} | "
            f"Page : {metadatas[result['index']]['page']}"
        )

    print(f"RERANK_THRESHOLD : {RERANK_THRESHOLD}")
    
    # Vérification de la pertinence du meilleur résultat
    
    # if ( not general_question and ( not ranked_documents 
    #         or ranked_documents[0]["score"] <= RERANK_THRESHOLD)):
    #     return {
    #         "documents": [[]],
    #         "metadatas": [[]],
    #         "distances": [[]],
    #         "rerank_scores": [[]]
    #     }
        
    # Préparation des résultats finaux

    final_documents = []
    final_metadatas = []
    final_distances = []
    rerank_scores = []

    for result in ranked_documents:

        index = result["index"]

        final_documents.append(result["document"])
        final_metadatas.append(metadatas[index])
        final_distances.append(distances[index])
        rerank_scores.append(result["score"])

    return {
        "documents": [final_documents],
        "metadatas": [final_metadatas],
        "distances": [final_distances],
        "rerank_scores": [rerank_scores]
    }


if __name__ == "__main__":

    # question = input("Pose ta question : ")

    # results = search_document(question)

    # documents = results["documents"][0]
    # metadatas = results["metadatas"][0]
    # distances = results["distances"][0]
    # rerank_scores = results["rerank_scores"][0]

    # if not documents:

    #     print("\nAucun chunk suffisamment pertinent trouvé.")

    # else:

    #     print("\n===== RÉSULTATS APRÈS RERANKING =====")

    #     for i in range(len(documents)):

    #         print(f"\n--- Résultat {i + 1} | Page {metadatas[i]['page']} ---")
    #         print(f"Distance Chroma : {distances[i]}")
    #         print(f"Score reranker : {rerank_scores[i]}")
    #         print(documents[i][:500])
    
    collection = create_vector_store()

    documents, metadatas = get_global_context(
        collection,
        num_chunks=8
    )

    print("\n===== CONTEXTE GLOBAL =====")

    for i in range(len(documents)):
        print(
            f"\n--- Chunk {i + 1} | "
            f"Page {metadatas[i]['page']} ---"
        )
        print(documents[i][:500])