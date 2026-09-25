import itertools

TAILLES     = [256, 512, 768, 1024]
OVERLAPS    = [0.0, 0.10, 0.20, 0.30]
STRATEGIES  = ["fixe", "recursif", "semantique"]

resultats = []

for taille, ratio, strategie in itertools.product(TAILLES, OVERLAPS, STRATEGIES):
    chunks = decouper(
        documents = corpus_test,
        taille    = taille,
        overlap   = int(taille * ratio),
        strategie = strategie,
    )

    index = reindexer(chunks)               # collection dediee, pas la prod
    scores = evaluer(questions_test, index) # hit@5, MRR, precision contextuelle

    resultats.append({
        "taille": taille, "overlap": ratio, "strategie": strategie, **scores,
    })

meilleure = max(resultats, key=lambda r: r["precision_contextuelle"])

# Note de cadrage : 4 x 4 x 3 = 48 configurations.
# Sur un millier de questions, comptez plusieurs heures de calcul,
# largement parallelisables. Commencez par un sous-ensemble :
# faites d'abord varier la taille seule, a strategie fixee.
