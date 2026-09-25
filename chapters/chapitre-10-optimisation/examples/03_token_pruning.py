from transformers import pipeline

class TokenPruner:
    def __init__(self, threshold=0.3):
        self.scorer = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        self.threshold = threshold

    def prune_context(self, context: str, question: str) -> str:
        """
        Elimine les phrases peu pertinentes pour la question.
        """
        sentences = context.split('. ')

        # Scorer chaque phrase par rapport a la question
        scores = []
        for sentence in sentences:
            result = self.scorer(
                sentence,
                [question],
                multi_class=True
            )
            scores.append(result['scores'][0])

        # Ne garder que les phrases pertinentes
        pruned = [
            sent for sent, score
            in zip(sentences, scores)
            if score > self.threshold
        ]

        return '. '.join(pruned)
