# Inventaire du code du manuscrit

Le manuscrit actif contient actuellement 111 environnements `lstlisting`.

| Chapitre | Blocs repérés | État |
|---:|---:|---|
| 1 | 0 | Contenu conceptuel |
| 2 | 4 | À inventorier |
| 3 | 16 | À inventorier |
| 4 | 10 | À inventorier |
| 5 | 14 | À inventorier |
| 6 | 17 | À inventorier |
| 7 | 4 | À inventorier |
| 8 | 10 | À inventorier |
| 9 | 18 | À inventorier |
| 10 | 6 | À inventorier |
| 11 | 6 | À inventorier |
| 12 | 6 | À inventorier |

## Cycle de traitement

1. Identifier la légende, le label et les dépendances du bloc.
2. Distinguer code complet, extrait pédagogique, pseudo-code et configuration.
3. Extraire le code exécutable vers un fichier nommé et testable.
4. Créer un notebook guidé qui importe ce fichier.
5. Ajouter un test sans appel payant par défaut.
6. Remplacer ensuite le bloc LaTeX inline par `\lstinputlisting` lorsque pertinent.
