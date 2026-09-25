import tiktoken


class BudgetContexte:
    """Selectionne les passages qui tiennent dans la fenetre."""

    def __init__(self, modele: str = "gpt-4o",
                 fenetre: int = 8000,
                 reserve_reponse: int = 1000,
                 minimum_utile: int = 150):
        self.encodeur = tiktoken.encoding_for_model(modele)
        self.fenetre = fenetre
        self.reserve_reponse = reserve_reponse
        self.minimum_utile = minimum_utile

    def compter(self, texte: str) -> int:
        return len(self.encodeur.encode(texte))

    def ajuster(self, passages: list, systeme: str,
                question: str) -> list:
        """Retourne le sous-ensemble de passages qui tient.

        Les passages doivent arriver TRIES par pertinence : la
        selection est gloutonne et s'arrete au premier qui deborde.
        """
        fixe = (self.compter(systeme)
                + self.compter(question)
                + self.reserve_reponse
                + 200)                  # marge pour le formatage

        disponible = self.fenetre - fixe
        if disponible <= 0:
            raise ValueError(
                "Instructions et question saturent deja la fenetre."
            )

        retenus, consomme = [], 0

        for passage in passages:
            cout = self.compter(passage.page_content)

            if consomme + cout <= disponible:
                retenus.append(passage)
                consomme += cout
                continue

            # Il ne tient pas. Le tronquer n'a de sens que s'il
            # reste assez de place pour un fragment exploitable ;
            # sinon un demi-passage induit le modele en erreur.
            reste = disponible - consomme
            if reste >= self.minimum_utile:
                jetons = self.encodeur.encode(passage.page_content)
                passage.page_content = (
                    self.encodeur.decode(jetons[:reste])
                    + " [...extrait tronque]"
                )
                retenus.append(passage)
            break

        return retenus
