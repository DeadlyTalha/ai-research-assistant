from sentence_transformers import SentenceTransformer
from chunker import split_text
from document_loader import extract_text_from_pdf, PDF_chemin


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts):
    model = load_embedding_model()

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


if __name__ == "__main__":

    text = extract_text_from_pdf(PDF_chemin)

   
    chunks = split_text(text)

    print(f"Nombre de chunks : {len(chunks)}")

    embeddings = generate_embeddings(chunks)

    print(f"Nombre d'embeddings : {len(embeddings)}")
    print(f"Dimension d'un embedding : {len(embeddings[0])}")

    print("\nPremier chunk :")
    print(chunks[0][:500])

    print("\nEmbedding du premier chunk :")
    print(embeddings[0])