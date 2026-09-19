import streamlit as st
from pathlib import Path

from ingest import ingest_pdf
from retriever import search_document
from llm import build_prompt, generate_response


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Research Assistant")

st.write(
    "Importez un document PDF puis posez vos questions "
    "à son sujet."
)


# =========================================================
# UPLOAD DU PDF
# =========================================================

st.subheader("📄 Document")

uploaded_file = st.file_uploader(
    "Choisissez un fichier PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    # Dossier de stockage
    documents_dir = Path("data/documents")
    documents_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Chemin du fichier
    pdf_path = documents_dir / uploaded_file.name

    # Sauvegarde du PDF
    with open(pdf_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    # Vérifie si le document vient d'être chargé
    if (
        "uploaded_file_name" not in st.session_state
        or st.session_state.uploaded_file_name != uploaded_file.name
    ):

        with st.spinner(
            "📚 Analyse et indexation du document..."
        ):

            info = ingest_pdf(pdf_path)

        st.session_state.uploaded_file_name = (
            uploaded_file.name
        )

        st.success(
            f"Document chargé avec succès : "
            f"{uploaded_file.name}"
        )

        st.info(
            f"{info['pages']} pages analysées — "
            f"{info['chunks']} chunks créés."
        )


# =========================================================
# QUESTION
# =========================================================

st.subheader("💬 Question")

question = st.text_input(
    "Posez une question sur le document :"
)


if question:

    results = search_document(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:

        st.warning(
            "Je ne trouve pas cette information "
            "dans le document."
        )

    else:

        prompt = build_prompt(
            question,
            documents,
            metadatas
        )

        with st.spinner("🤖 Génération de la réponse..."):

            response = generate_response(prompt)

        st.subheader("Réponse")

        st.write(response)

        st.subheader("Sources")

        pages = []

        for metadata in metadatas:

            page = metadata["page"]

            if page not in pages:
                pages.append(page)

        for page in pages:
            st.write(f"- Page {page}")