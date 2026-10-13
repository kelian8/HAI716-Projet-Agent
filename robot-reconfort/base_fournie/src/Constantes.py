EMOTIONS_ORDRE = [
    "joie", "confiance", "peur", "surprise",
    "tristesse", "degout", "colere", "anticipation",
]
INTENSITES_ORDRE = ["faible", "moyenne", "forte"]

# {"joie": 0, "confiance": 1, ...}
COLONNE_EMOTION: dict[str, int] = {nom: i for i, nom in enumerate(EMOTIONS_ORDRE)}
# {"faible": 0, "moyenne": 1, "forte": 2}
LIGNE_INTENSITE: dict[str, int] = {nom: i for i, nom in enumerate(INTENSITES_ORDRE)}