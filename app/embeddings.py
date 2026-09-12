from sentence_transformers import SentenceTransformer
from chunker import create_chunks_from_pages
from document_loader import extract_pages_from_pdf, PDF_chemin


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
    pages = extract_pages_from_pdf(PDF_chemin)

    chunks = create_chunks_from_pages(pages)

    print(f"Nombre de chunks : {len(chunks)}")

    chunk_texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(chunk_texts)

    print(f"Nombre d'embeddings : {len(embeddings)}")
    print(f"Dimension d'un embedding : {len(embeddings[0])}")

    print("\nPremier chunk :")
    print(chunks[0]["text"][:500])

    print("\nEmbedding du premier chunk :")
    print(embeddings[0])