from dataclasses import dataclass


@dataclass(frozen=True)          # frozen : l'objet ne change plus apres creation
class ChunkEnrichi:
    """
    L'unite finale, prete a vectoriser.
    Deux sorties distinctes : ce qu'on embarque, ce qu'on stocke.
    """
    texte: str
    source: str
    chemin: str            # "Section: Echecs de paiement > Cartes refusees"
    index: int
    page: int
    debut_char: int
    fin_char: int
    langue: str = "fr"

    def texte_a_vectoriser(self) -> str:
        """
        Context Prepending : l'en-tete hierarchique precede le texte.
        C'est CETTE chaine qui part au modele d'embedding, pas self.texte.
        """
        entete = f"Document: {self.source} > {self.chemin}"
        return f"{entete}\n\n{self.texte}"

    def metadonnees(self) -> dict:
        """
        Stocke a cote du vecteur, jamais vectorise.
        Sert au filtrage prealable, a la citation et a la fusion.
        """
        return {
            "source":     self.source,
            "chemin":     self.chemin,
            "index":      self.index,
            "page":       self.page,
            "debut_char": self.debut_char,
            "fin_char":   self.fin_char,
            "langue":     self.langue,
        }


if __name__ == "__main__":
    chunk = ChunkEnrichi(
        texte="Vérifiez le plafond de la carte.",
        source="manuel_paiement.md",
        chemin="Paiement > Cartes refusées",
        index=0,
        page=3,
        debut_char=120,
        fin_char=154,
    )
    print(chunk.texte_a_vectoriser())
    print(chunk.metadonnees())
