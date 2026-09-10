from pathlib import Path
from pypdf import PdfReader


PDF_chemin = Path("data/documents/Intelligence_arti_guide_de_survie.pdf")


def extract_pages_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            pages.append({
                "page": page_number,
                "text": page_text
            })

    return pages


if __name__ == "__main__":

    pages = extract_pages_from_pdf(PDF_chemin)

    print(f"Nombre de pages : {len(pages)}")

    for page in pages[:3]:
        print(f"\n--- Page {page['page']} ---")
        print(page["text"][:500])