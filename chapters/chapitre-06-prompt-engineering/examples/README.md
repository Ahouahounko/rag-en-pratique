# Exemples du chapitre 6

Les fichiers de ce dossier sont extraits automatiquement du manuscrit. 
Le contenu est conservé tel quel afin de permettre sa revue avant transformation 
en exemple autonome ou en notebook exécutable.

| # | Label LaTeX | Légende | Type | Fichier | Validation |
|---:|---|---|---|---|---|
| 01 | `lst:prompt_minimal` | Le prompt RAG minimal viable | python | [`01_prompt_minimal.py`](01_prompt_minimal.py) | syntaxe validée |
| 02 | `lst:format_simple` | Format textuel simple compact et lisible | python | [`02_format_simple.py`](02_format_simple.py) | syntaxe validée |
| 03 | `lst:format_balise` | Format balisé --- métadonnées riches et frontières explicites | python | [`03_format_balise.py`](03_format_balise.py) | syntaxe validée |
| 04 | `lst:format_annote` | Format annoté pertinence qualitative et filtrage | python | [`04_format_annote.py`](04_format_annote.py) | syntaxe validée |
| 05 | `lst:verif_citations` | Vérification des citations produites par le modèle | python | [`05_verif_citations.py`](05_verif_citations.py) | syntaxe validée |
| 06 | `lst:budget_tokens` | Ajustement des passages au budget de tokens disponible | python | [`06_budget_tokens.py`](06_budget_tokens.py) | syntaxe validée |
| 07 | `lst:cot_rag` | Prompt Chain-of-Thought pour RAG | python | [`07_cot_rag.py`](07_cot_rag.py) | syntaxe validée |
| 08 | `lst:step_back` | Step-back prompting de la question spécifique au principe applicable | python | [`08_step_back.py`](08_step_back.py) | syntaxe validée |
| 09 | `lst:verification` | Vérification d'ancrage affirmation par affirmation | python | [`09_verification.py`](09_verification.py) | syntaxe validée |
| 10 | `lst:few_shot` | Few-shot deux démonstrations valant mieux qu'une consigne | python | [`10_few_shot.py`](10_few_shot.py) | syntaxe validée |
| 11 | `lst:rag_conversationnel` | RAG conversationnel condensation et mémoire bornée | python | [`11_rag_conversationnel.py`](11_rag_conversationnel.py) | syntaxe validée |
| 12 | `lst:refus` | Refus gradué trois niveaux de couverture | python | [`12_refus.py`](12_refus.py) | syntaxe validée |
| 13 | `lst:refus_amont` | Refus décidé avant génération, sur le score de retrieval | python | [`13_refus_amont.py`](13_refus_amont.py) | syntaxe validée |
| 14 | `lst:conflits` | Traitement explicite des contradictions entre extraits | python | [`14_conflits.py`](14_conflits.py) | syntaxe validée |
| 15 | `lst:synthese` | Synthèse structurée par thèmes | python | [`15_synthese.py`](15_synthese.py) | syntaxe validée |
| 16 | `lst:injection` | Neutralisation du contenu récupéré avant injection | python | [`16_injection.py`](16_injection.py) | syntaxe validée |
| 17 | `lst:regression_prompts` | Jeu de régression pour prompts, en pseudo-code | text | [`17_regression_prompts.txt`](17_regression_prompts.txt) | à valider |

## Convention de validation

- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;
- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;
- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.
