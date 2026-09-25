"""Extrait les environnements LaTeX lstlisting vers le dépôt compagnon.

Le script est volontairement sans dépendance externe. Il conserve le contenu
des blocs tel qu'il apparaît dans le manuscrit et produit un inventaire Markdown
pour chaque chapitre.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chapter:
    number: int
    source: str
    destination: str


CHAPTERS = (
    Chapter(1, "chapitre1_ia_generative_et_llm3.tex", "chapitre-01-fondations-llm"),
    Chapter(2, "chapitre2_introduction_rag_naive2.tex", "chapitre-02-premier-rag"),
    Chapter(3, "chapitre3_preparation_donnees_chunking_v3.tex", "chapitre-03-donnees-et-chunking"),
    Chapter(4, "chapitre4_retrieval_avance_v3.tex", "chapitre-04-retrieval-avance"),
    Chapter(5, "chapitre5_bases_vectorielles_v3.tex", "chapitre-05-bases-vectorielles"),
    Chapter(6, "chapitre6_prompt_engineering_v2.tex", "chapitre-06-prompt-engineering"),
    Chapter(7, "chapitre7_cadrer_evaluation_metriques_v2.tex", "chapitre-07-evaluation"),
    Chapter(8, "chapitre8_mesurer_diagnostiquer_surveiller_v2.tex", "chapitre-08-observabilite"),
    Chapter(9, "chapitre9_docurag_v2.tex", "chapitre-09-docurag"),
    Chapter(10, "chapitre10_optimiser_v2.tex", "chapitre-10-optimisation"),
    Chapter(11, "chapitre11_securiser_fiabiliser_v2.tex", "chapitre-11-securite"),
    Chapter(12, "chapitre12_bonnes_pratiques_v2.tex", "chapitre-12-bonnes-pratiques"),
)

BEGIN = r"\begin{lstlisting}"
END = r"\end{lstlisting}"


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = value.lower().replace("lst:", "")
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "exemple"


def option_value(options: str, key: str) -> str | None:
    match = re.search(rf"(?:^|,)\s*{re.escape(key)}\s*=\s*", options)
    if not match:
        return None
    start = match.end()
    if start < len(options) and options[start] == "{":
        depth = 0
        for index in range(start, len(options)):
            if options[index] == "{":
                depth += 1
            elif options[index] == "}":
                depth -= 1
                if depth == 0:
                    return options[start + 1 : index].strip()
    return options[start:].split(",", 1)[0].strip()


def listings(source: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    cursor = 0
    while True:
        begin = source.find(BEGIN, cursor)
        if begin < 0:
            break
        options_start = begin + len(BEGIN)
        options = ""
        content_start = options_start
        if options_start < len(source) and source[options_start] == "[":
            options_end = source.find("]", options_start + 1)
            if options_end < 0:
                raise ValueError("Options lstlisting non fermées")
            options = source[options_start + 1 : options_end]
            content_start = options_end + 1
        if source.startswith("\r\n", content_start):
            content_start += 2
        elif content_start < len(source) and source[content_start] == "\n":
            content_start += 1
        end = source.find(END, content_start)
        if end < 0:
            raise ValueError("Environnement lstlisting non fermé")
        content = source[content_start:end].rstrip() + "\n"
        result.append((options, content))
        cursor = end + len(END)
    return result


def classify(options: str, content: str) -> tuple[str, str]:
    declared = (option_value(options, "language") or "").lower()
    stripped = content.lstrip()
    if declared in {"bash", "sh", "shell"}:
        return "bash", ".sh"
    if declared in {"sql"}:
        return "sql", ".sql"
    if declared in {"json"}:
        return "json", ".json"
    if declared in {"yaml", "yml"}:
        return "yaml", ".yml"
    if declared in {"python", "python3"}:
        return "python", ".py"
    if stripped.startswith(("{", "[")):
        try:
            json.loads(content)
            return "json", ".json"
        except json.JSONDecodeError:
            pass
    if re.search(r"(?m)^\s*(from\s+\S+\s+import|import\s+\S+|def\s+\w+|class\s+\w+)", content):
        return "python", ".py"
    if re.search(r"(?mi)^\s*(pip install|python -m|docker |docker-compose|curl |export |git )", content):
        return "bash", ".sh"
    if re.search(r"(?mi)^\s*(select|create table|insert into|with\s+\w+\s+as)\b", content):
        return "sql", ".sql"
    if re.search(r"(?m)^\s*(services:|version:|apiVersion:|kind:)", content):
        return "yaml", ".yml"
    return "text", ".txt"


def python_status(content: str) -> str:
    try:
        ast.parse(content)
    except SyntaxError:
        return "extrait pédagogique"
    return "syntaxe validée"


def clean_markdown(value: str) -> str:
    value = value.replace("\n", " ").replace("|", "\\|")
    return re.sub(r"\s+", " ", value).strip()


def extract_chapter(chapter: Chapter, manuscript: Path, repository: Path) -> int:
    source_path = manuscript / chapter.source
    target = repository / "chapters" / chapter.destination / "examples"
    target.mkdir(parents=True, exist_ok=True)
    extracted = listings(source_path.read_text(encoding="utf-8-sig"))
    rows: list[str] = []
    used: set[str] = set()

    for index, (options, content) in enumerate(extracted, start=1):
        label = option_value(options, "label") or f"lst:chapitre{chapter.number}_{index:02d}"
        caption = option_value(options, "caption") or "Exemple sans légende"
        language, extension = classify(options, content)
        base = slugify(label)
        if base in used:
            base = f"{base}_{index:02d}"
        used.add(base)
        filename = f"{index:02d}_{base}{extension}"
        (target / filename).write_text(content, encoding="utf-8", newline="\n")
        status = python_status(content) if language == "python" else "à valider"
        rows.append(
            f"| {index:02d} | `{clean_markdown(label)}` | "
            f"{clean_markdown(caption)} | {language} | "
            f"[`{filename}`]({filename}) | {status} |"
        )

    manifest = [
        f"# Exemples du chapitre {chapter.number}\n",
        "Les fichiers de ce dossier sont extraits automatiquement du manuscrit. ",
        "Le contenu est conservé tel quel afin de permettre sa revue avant transformation ",
        "en exemple autonome ou en notebook exécutable.\n",
        "| # | Label LaTeX | Légende | Type | Fichier | Validation |",
        "|---:|---|---|---|---|---|",
        *rows,
        "",
        "## Convention de validation\n",
        "- **syntaxe validée** : le fichier Python passe l'analyse syntaxique ;",
        "- **extrait pédagogique** : le bloc est partiel, contient des ellipses ou demande un contexte ;",
        "- **à valider** : commande, configuration, prompt ou autre contenu à tester manuellement.",
        "",
    ]
    (target / "README.md").write_text("\n".join(manifest), encoding="utf-8", newline="\n")

    chapter_readme = repository / "chapters" / chapter.destination / "README.md"
    current = chapter_readme.read_text(encoding="utf-8").rstrip()
    marker = "## Code du manuscrit"
    if marker in current:
        current = current.split(marker, 1)[0].rstrip()
    current += (
        f"\n\n{marker}\n\n"
        f"Ce chapitre contient **{len(extracted)} bloc(s) de code** extrait(s) du manuscrit. "
        f"Consultez [l'inventaire des exemples](examples/README.md).\n"
    )
    chapter_readme.write_text(current, encoding="utf-8", newline="\n")
    return len(extracted)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", required=True, type=Path)
    parser.add_argument("--repository", required=True, type=Path)
    args = parser.parse_args()
    total = 0
    for chapter in CHAPTERS:
        count = extract_chapter(chapter, args.manuscript, args.repository)
        print(f"Chapitre {chapter.number:02d}: {count:02d} bloc(s)")
        total += count
    print(f"Total: {total} bloc(s)")


if __name__ == "__main__":
    main()
