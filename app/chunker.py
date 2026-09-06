def split_text(text,chunk_size=1000,overlap=200):
    chunks =[]
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        start = end - overlap
        
    return chunks

if __name__ == "__main__":
    from document_loader import extract_text_from_pdf, PDF_chemin

    # 1. Extraction du texte
    text = extract_text_from_pdf(PDF_chemin)

    print("=" * 60)
    print("INSPECTION DU DOCUMENT")
    print("=" * 60)

    print(f"Nombre de caractères : {len(text)}")

    # 2. Création des chunks
    chunks = split_text(text)

    print(f"Nombre de chunks : {len(chunks)}")

    # 3. Statistiques
    sizes = [len(chunk) for chunk in chunks]

    print(f"Taille minimale : {min(sizes)} caractères")
    print(f"Taille maximale : {max(sizes)} caractères")
    print(f"Taille moyenne  : {sum(sizes) // len(sizes)} caractères")

    # 4. Affichage des premiers chunks
    print("\n" + "=" * 60)
    print("APERÇU DES CHUNKS")
    print("=" * 60)

    for i, chunk in enumerate(chunks[:10], start=1):
        print(f"\n{'-' * 60}")
        print(f"CHUNK {i}")
        print(f"Taille : {len(chunk)} caractères")
        print(f"{'-' * 60}")
        print(chunk)
  
