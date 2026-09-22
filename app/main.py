import streamlit as st
from pathlib import Path

from ingest import ingest_pdf
from retriever import search_document
from llm import build_prompt, generate_response, build_global_prompt
from query_classifier import classify_question


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "document_info" not in st.session_state:
    st.session_state.document_info = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 AI Research Assistant")

    st.markdown("---")

    st.subheader("📄 Document")

    uploaded_file = st.file_uploader(
        "Importer un document PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        documents_dir = Path("data/documents")
        documents_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        pdf_path = documents_dir / uploaded_file.name

        # Sauvegarde du PDF
        with open(pdf_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Indexation uniquement si nouveau document
        if (
            st.session_state.uploaded_file_name
            != uploaded_file.name
        ):
            st.session_state.messages = []
            
            with st.spinner(
                "📚 Analyse du document..."
            ):

                info = ingest_pdf(pdf_path)

            st.session_state.uploaded_file_name = (
                uploaded_file.name
            )

            st.session_state.document_info = info

            st.success("Document prêt !")

    # Informations sur le document
    if st.session_state.uploaded_file_name:

        st.markdown("---")
        
        if st.button("🗑️ Nouvelle conversation", use_container_width=True):

            st.session_state.messages = []

            st.rerun()
            
        st.subheader("🟢 Document actif")

        st.write(
            f"**{st.session_state.uploaded_file_name}**"
        )

        if st.session_state.document_info:

            info = st.session_state.document_info

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Pages",
                    info["pages"]
                )

            with col2:
                st.metric(
                    "Chunks",
                    info["chunks"]
                )

    else:

        st.info(
            "Importez un PDF pour commencer."
        )




# =========================================================
# QUESTION
# =========================================================

# =========================================================
# HISTORIQUE DE LA CONVERSATION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# PAGE PRINCIPALE
# =========================================================

st.title("📚 Posez vos questions au document")

st.write(
    "Interrogez votre document en langage naturel."
)


# =========================================================
# AFFICHAGE DE L'HISTORIQUE
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

if st.session_state.uploaded_file_name:

    question = st.chat_input(
        "Posez votre question sur le document..."
    )

    if question:

        # -----------------------------------------------
        # Message utilisateur
        # -----------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)


        # -----------------------------------------------
        # Recherche dans le document
        # -----------------------------------------------

        results = search_document(question)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]


        # -----------------------------------------------
        # Aucun résultat
        # -----------------------------------------------

        if not documents:

            response = (
                "Je ne trouve pas cette information "
                "dans le document."
            )

            with st.chat_message("assistant"):
                st.warning(response)


        # -----------------------------------------------
        # Réponse trouvée
        # -----------------------------------------------

        else:

            question_type = classify_question(question)

            if question_type == "GLOBAL":

                prompt = build_global_prompt(
                    question,
                    documents,
                    metadatas
                )

            else:

                prompt = build_prompt(
                    question,
                    documents,
                    metadatas
                )

            with st.chat_message("assistant"):

                with st.spinner(
                    "🤖 Recherche dans le document..."
                ):

                    print("\n===== CONTEXTE ENVOYÉ À QWEN =====")

                    for i, document in enumerate(documents):
                        print(f"\n--- CHUNK {i+1} | PAGE {metadatas[i]['page']} ---")
                        print(document)
                    
                    print("\n===== PROMPT ENVOYÉ À QWEN =====")
                    print(prompt)
                    print("===== FIN PROMPT =====")
                    response = generate_response(prompt)

                st.markdown(response)


                # ---------------------------------------
                # Sources
                # ---------------------------------------

                pages = []

                for metadata in metadatas:

                    page = metadata["page"]

                    if page not in pages:
                        pages.append(page)


                if pages:

                    st.markdown("**📚 Sources**")

                    for page in pages:

                        st.caption(
                            f"📄 Page {page}"
                        )


        # -----------------------------------------------
        # Sauvegarde de la réponse
        # -----------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


else:

    st.info(
        "👈 Importez d'abord un document PDF "
        "dans la barre latérale."
    )