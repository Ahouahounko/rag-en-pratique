# Inventaire du code du manuscrit

Le manuscrit actif contient 111 environnements `lstlisting`, tous extraits dans
les dossiers `examples/` des chapitres. Les fichiers conservent leur label et
leur légende LaTeX dans un inventaire local.

| Chapitre | Blocs | Inventaire | État |
|---:|---:|---|---|
| 1 | 0 | [Fondations LLM](../chapters/chapitre-01-fondations-llm/examples/README.md) | Contenu conceptuel |
| 2 | 4 | [Premier RAG](../chapters/chapitre-02-premier-rag/examples/README.md) | Extrait |
| 3 | 16 | [Données et chunking](../chapters/chapitre-03-donnees-et-chunking/examples/README.md) | Extrait |
| 4 | 10 | [Retrieval avancé](../chapters/chapitre-04-retrieval-avance/examples/README.md) | Extrait |
| 5 | 14 | [Bases vectorielles](../chapters/chapitre-05-bases-vectorielles/examples/README.md) | Extrait |
| 6 | 17 | [Prompt engineering](../chapters/chapitre-06-prompt-engineering/examples/README.md) | Extrait |
| 7 | 4 | [Évaluation](../chapters/chapitre-07-evaluation/examples/README.md) | Extrait |
| 8 | 10 | [Observabilité](../chapters/chapitre-08-observabilite/examples/README.md) | Extrait |
| 9 | 18 | [DocuRAG](../chapters/chapitre-09-docurag/examples/README.md) | Extrait |
| 10 | 6 | [Optimisation](../chapters/chapitre-10-optimisation/examples/README.md) | Extrait |
| 11 | 6 | [Sécurité](../chapters/chapitre-11-securite/examples/README.md) | Extrait |
| 12 | 6 | [Bonnes pratiques](../chapters/chapitre-12-bonnes-pratiques/examples/README.md) | Extrait |

## Première validation

- 96 fichiers Python avec syntaxe validée ;
- 13 blocs textuels ou prompts à valider ;
- 1 script shell à valider ;
- 1 configuration YAML à valider.

## Cycle de traitement

1. Examiner les dépendances et les entrées attendues par chaque fichier extrait.
2. Distinguer les exemples autonomes des extraits nécessitant un contexte.
3. Ajouter un test sans appel payant par défaut.
4. Créer un notebook guidé qui importe les fichiers validés.
5. Remplacer ensuite le bloc LaTeX inline par `\lstinputlisting` lorsque pertinent.
