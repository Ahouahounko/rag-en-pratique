# Exemples du chapitre 6

| # | Sujet | Fichier | Exécution |
|---:|---|---|---|
| 01 | Prompt RAG minimal | [`01_prompt_minimal.py`](01_prompt_minimal.py) | OpenAI facultatif |
| 02 | Format textuel simple | [`02_format_simple.py`](02_format_simple.py) | locale |
| 03 | Format balisé | [`03_format_balise.py`](03_format_balise.py) | locale |
| 04 | Pertinence qualitative | [`04_format_annote.py`](04_format_annote.py) | locale |
| 05 | Validation des citations | [`05_verif_citations.py`](05_verif_citations.py) | locale |
| 06 | Budget de tokens | [`06_budget_tokens.py`](06_budget_tokens.py) | locale |
| 07 | Analyse documentaire structurée | [`07_cot_rag.py`](07_cot_rag.py) | OpenAI |
| 08 | Step-back prompting | [`08_step_back.py`](08_step_back.py) | OpenAI |
| 09 | Vérification d'ancrage | [`09_verification.py`](09_verification.py) | OpenAI |
| 10 | Few-shot | [`10_few_shot.py`](10_few_shot.py) | OpenAI |
| 11 | RAG conversationnel | [`11_rag_conversationnel.py`](11_rag_conversationnel.py) | OpenAI |
| 12 | Refus gradué | [`12_refus.py`](12_refus.py) | OpenAI |
| 13 | Refus avant génération | [`13_refus_amont.py`](13_refus_amont.py) | local ou OpenAI |
| 14 | Contradictions | [`14_conflits.py`](14_conflits.py) | OpenAI |
| 15 | Synthèse thématique | [`15_synthese.py`](15_synthese.py) | OpenAI |
| 16 | Neutralisation d'injection | [`16_injection.py`](16_injection.py) | locale |
| 17 | Régression des prompts | [`17_regression_prompts.py`](17_regression_prompts.py) | locale |

Le module partagé `rag_en_pratique.prompting` centralise le type `Passage`, le
formatage simple et l'appel injectable à la Responses API.

## Installation

```bash
pip install -e ".[prompting]"
```

Pour appeler OpenAI :

```bash
pip install -e ".[openai]"
```
