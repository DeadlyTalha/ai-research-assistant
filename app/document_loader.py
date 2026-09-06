from pathlib import Path
from pypdf import PdfReader

PDF_chemin = Path("data/documents/Intelligence_arti_guide_de_survie.pdf")

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    
    text = ""
    
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        
        if page_text:
            text += f"\n--- Page {page_number} ---\n"
            text += page_text
    
    return text

if __name__ == "__main__":
    text = extract_text_from_pdf(PDF_chemin)
    
    print(f"Le nombre de caractere : {len(text)}")
    print("\nPremiers caracteres du document:\n")
    print(text[:3000])