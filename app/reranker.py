from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"


def load_reranker():
    return CrossEncoder(MODEL_NAME)


def rerank_documents(question, documents, top_k=3):
    # Reclasse les documents selon leur pertinence par rapport à la question.
    
    model = load_reranker()

    pairs = [
        [question, document]
        for document in documents
    ]

    scores = model.predict(pairs)
    
    ranked = sorted(
        [
            {
                "document": document,
                "score": float(score),
                "index": index
            }
            for index, (document, score) in enumerate(
                zip(documents, scores)
            )
        ],
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:top_k]