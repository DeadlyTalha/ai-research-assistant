from embeddings import load_embedding_model
from vector_store import create_vector_store
from reranker import rerank_documents


DISTANCE_THRESHOLD = 1.2
RETRIEVAL_TOP_K = 10
FINAL_TOP_K = 3


def search_document(question):
    """
    Recherche les chunks pertinents en deux étapes :

    1. Retrieval avec ChromaDB
    2. Reranking avec un CrossEncoder
    """

    collection = create_vector_store()
    embedding_model = load_embedding_model()

    # --------------------------------------------------
    # 1. Retrieval avec ChromaDB
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 2. Seuil de distance
    # --------------------------------------------------

    if distances[0] > DISTANCE_THRESHOLD:
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "rerank_scores": [[]]
        }

    # --------------------------------------------------
    # 3. Reranking
    # --------------------------------------------------

    ranked_documents = rerank_documents(
        question,
        documents,
        top_k=FINAL_TOP_K
    )

    # --------------------------------------------------
    # 4. Préparation des résultats finaux
    # --------------------------------------------------

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

    question = input("Pose ta question : ")

    results = search_document(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    rerank_scores = results["rerank_scores"][0]

    if not documents:

        print("\nAucun chunk suffisamment pertinent trouvé.")

    else:

        print("\n===== RÉSULTATS APRÈS RERANKING =====")

        for i in range(len(documents)):

            print(f"\n--- Résultat {i + 1} | Page {metadatas[i]['page']} ---")
            print(f"Distance Chroma : {distances[i]}")
            print(f"Score reranker : {rerank_scores[i]}")
            print(documents[i][:500])