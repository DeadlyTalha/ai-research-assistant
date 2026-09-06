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
Version 0.1 — Configuration initiale
 Création de la structure du projet
 Configuration de l'environnement Python
 Ajout d'un document PDF
 Extraction du texte depuis un fichier PDF
 Initialisation du dépôt Git
 Connexion du projet à GitHub