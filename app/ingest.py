from pathlib import Path

from document_loader import extract_pages_from_pdf
from chunker import create_chunks_from_pages
from embeddings import load_embedding_model
from vector_store import create_vector_store


def ingest_pdf(pdf_path):
    """
    Traite un fichier PDF et l'enregistre dans ChromaDB.
    """

    # 1. Extraction des pages
    pages = extract_pages_from_pdf(pdf_path)

    # 2. Création des chunks
    chunks = create_chunks_from_pages(pages)

    # 3. Génération des embeddings
    model = load_embedding_model()

    chunk_texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        chunk_texts,
        show_progress_bar=False
    )

    # 4. Récupération de la collection
    collection = create_vector_store()

    # 5. Suppression des anciennes données
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # 6. Ajout du nouveau document
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=chunk_texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {"page": chunk["page"]}
            for chunk in chunks
        ]
    )

    return {
        "pages": len(pages),
        "chunks": len(chunks)
    }