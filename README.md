# AI Research Assistant

Assistant de recherche intelligent basé sur l'architecture **Retrieval-Augmented Generation (RAG)**, permettant de poser des questions sur des documents et d'obtenir des réponses générées à partir des informations extraites de ces documents.

## 🎯 Objectif du projet

L'objectif de ce projet est de développer un assistant intelligent capable de comprendre et de répondre à des questions concernant des documents fournis par l'utilisateur.

Contrairement à un LLM qui s'appuie uniquement sur les connaissances acquises lors de son entraînement, notre assistant récupère d'abord les informations pertinentes dans les documents avant de générer une réponse.

Cette approche permet d'obtenir des réponses davantage **contextualisées, pertinentes et basées sur les sources fournies**.

## Fonctionnement

Le projet repose sur une architecture **Retrieval-Augmented Generation (RAG)** :

```text
Documents PDF
     ↓
Extraction du texte
     ↓
Découpage du texte (Chunking)
     ↓
Création des Embeddings
     ↓
Base de données vectorielle
     ↓
Question de l'utilisateur
     ↓
Recherche sémantique
     ↓
Contexte pertinent
     ↓
LLM
     ↓
Réponse générée 
```

## 🛠️ Technologies

Les principales technologies utilisées ou prévues dans le projet sont :

Python
PyPDF
Embeddings
Base de données vectorielle
Large Language Models (LLM)
Retrieval-Augmented Generation (RAG)
Streamlit
Git & GitHub

Les technologies seront ajoutées et précisées progressivement au cours du développement.

## 🚀 État d'avancement
### Version 0.1 — Configuration initiale
- [x] Création de la structure du projet
- [x] Configuration de l'environnement Python*
- [x] Ajout d'un document PDF
- [x] Extraction du texte depuis un fichier PDF
- [x] Initialisation du dépôt Git
- [x] Connexion du projet à GitHub

### Version 0.2 — Préparation des documents

- [x] Découpage du texte en chunks
- [x] Conservation des métadonnées des chunks
- [x] Association des chunks avec leur numéro de page
- [x] Inspection des chunks générés

### Version 0.3 — Embeddings et recherche sémantique

- [x] Intégration du modèle d'embeddings `all-MiniLM-L6-v2`
- [x] Génération des embeddings des chunks
- [x] Mise en place de ChromaDB
- [x] Stockage des chunks et de leurs embeddings
- [x] Implémentation de la recherche sémantique
- [x] Récupération des chunks les plus pertinents

### Version 0.4 — Génération avec un LLM

- [x] Intégration d'un LLM local avec Ollama
- [x] Intégration du modèle `Qwen3.5 4B`
- [x] Connexion du système de retrieval au LLM
- [x] Construction d'un contexte à partir des chunks récupérés
- [x] Génération de réponses basées sur le document
- [x] Ajout des numéros de page comme sources
- [x] Gestion des questions dont la réponse n'est pas présente dans le document

### Prochaines étapes

- [ ] Améliorer la pertinence de la recherche avec un seuil de similarité
- [ ] Ajouter une interface utilisateur avec Streamlit
- [ ] Permettre l'ajout de plusieurs documents
- [ ] Ajouter l'historique des conversations
- [ ] Améliorer l'affichage des sources
- [ ] Évaluer la qualité des réponses du système RAG
- [ ] Améliorer l'expérience utilisateur
