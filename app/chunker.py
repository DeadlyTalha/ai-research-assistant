def split_text(text, chunk_size=1000, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def create_chunks_from_pages(pages, chunk_size=1000, overlap=200):

    chunks = []

    chunk_id = 0

    for page in pages:

        page_chunks = split_text(
            page["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk in page_chunks:

            chunks.append({
                "id": f"chunk_{chunk_id}",
                "text": chunk,
                "page": page["page"]
            })

            chunk_id += 1

    return chunks


if __name__ == "__main__":

    from document_loader import extract_pages_from_pdf, PDF_PATH

    pages = extract_pages_from_pdf(PDF_PATH)

    chunks = create_chunks_from_pages(pages)

    print(f"Nombre de pages : {len(pages)}")
    print(f"Nombre de chunks : {len(chunks)}")

    for chunk in chunks[:5]:

        print("\n" + "-" * 60)
        print(f"ID : {chunk['id']}")
        print(f"Page : {chunk['page']}")
        print(f"Taille : {len(chunk['text'])} caractères")
        print("-" * 60)

        print(chunk["text"])