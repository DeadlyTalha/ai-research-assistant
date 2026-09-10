import chromadb

from document_loader import extract_pages_from_pdf, PDF_chemin
from chunker import create_chunks_from_pages
from embeddings import load_embedding_model


COLLECTION_NAME = "research_documents"


def create_vector_store():

    client = chromadb.PersistentClient(
        path="data/chroma"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


if __name__ == "__main__":

    # 1. Extraire les pages du PDF
    pages = extract_pages_from_pdf(PDF_chemin)

    print(f"Nombre de pages : {len(pages)}")

    # 2. Créer les chunks avec leurs métadonnées
    chunks = create_chunks_from_pages(pages)

    print(f"Nombre de chunks : {len(chunks)}")

    # 3. Extraire uniquement les textes
    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # 4. Générer les embeddings
    model = load_embedding_model()

    embeddings = model.encode(
        chunk_texts,
        show_progress_bar=True
    )

    # 5. Créer la collection
    collection = create_vector_store()

    # 6. Ajouter les chunks + embeddings + métadonnées
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=chunk_texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "page": chunk["page"]
            }
            for chunk in chunks
        ]
    )

    print("\n-- OK !Données enregistrées dans ChromaDB. --")
    print(f"Nombre de documents : {collection.count()}")