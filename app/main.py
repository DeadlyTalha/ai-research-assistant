import streamlit as st

from retriever import search_document
from llm import build_prompt, generate_response


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Research Assistant")

st.write(
    "Posez une question sur votre document "
    "et obtenez une réponse basée sur son contenu."
)

question = st.text_input("Posez votre question :")

if question:
    results = search_document(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        st.warning(
            "Je ne trouve pas cette information dans le document."
        )

    else:
        prompt = build_prompt(
            question,
            documents,
            metadatas
        )

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