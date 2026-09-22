from embeddings import load_embedding_model

GENERAL_EXAMPLES = [
    "De quoi parle ce document ?",
    "Quel est le sujet principal de ce document ?",
    "Quel est le thème général de ce livre ?",
    "Peux-tu résumer globalement ce document ?",
    "Quelle est l'idée générale de cet ouvrage ?",
    "Quel est le contenu général de ce document ?",
]

SYNTHESIS_EXAMPLES = [
    "Quels sont les principaux événements présentés dans le document ?",
    "Quels sont les points importants abordés dans ce document ?",
    "Peux-tu faire une synthèse des différentes idées du document ?",
    "Quels sont les grands thèmes abordés dans cet ouvrage ?",
    "Présente-moi les principaux éléments développés dans le document.",
]


def classify_question(question):
    model = load_embedding_model()

    question_embedding = model.encode([question])

    general_embeddings = model.encode(GENERAL_EXAMPLES)
    synthesis_embeddings = model.encode(SYNTHESIS_EXAMPLES)

    general_scores = model.similarity(
        question_embedding,
        general_embeddings
    )[0]

    synthesis_scores = model.similarity(
        question_embedding,
        synthesis_embeddings
    )[0]

    general_score = float(general_scores.max())
    synthesis_score = float(synthesis_scores.max())

    if general_score > synthesis_score and general_score >= 0.55:
        return "GLOBAL"

    if synthesis_score >= 0.55:
        return "SYNTHESIS"

    return "FACTUAL"

if __name__ == "__main__":
    questions = [
        "De quoi parle ce document ?",
        "Peux-tu me donner une vue d'ensemble de ce livre ?",
        "Quand a eu lieu la chute de l'empire d'Occident ?",
        "Quels sont les principaux événements présentés dans ce document ?",
    ]

    for question in questions:
        print(f"\nQuestion : {question}")
        print(f"Type : {classify_question(question)}")