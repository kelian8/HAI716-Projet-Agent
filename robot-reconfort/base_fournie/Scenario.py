import reconfort_io as rio
from Carte import Carte
# from Armoire import Armoire   # à décommenter quand la classe Armoire existera


class Scenario:
    def __init__(self, nom, carte, armoire, demandes):
        self.nom = nom
        self.carte = carte
        self.armoire = armoire
        self.demandes = demandes

    @classmethod
    def _from_json(cls, chemin):
        scenario_donnees = rio.charger_carte(chemin)  # même fonction générique de lecture JSON

        # La carte est désérialisée à partir de son propre fichier,
        # construit à partir du nom donné dans le scénario
        chemin_carte = "cartes/" + scenario_donnees["carte"] + ".json"
        carte = Carte._from_json(chemin_carte)

        # Idem à terme pour l'armoire : le scénario ne stocke qu'un nom,
        # on va chercher le fichier correspondant et on désérialise
        # chemin_armoire = "armoires/" + scenario_donnees["armoire"] + ".json"
        # armoire = Armoire._from_json(chemin_armoire)
        armoire = scenario_donnees["armoire"]  # provisoire : juste le nom en string pour l'instant

        demandes = [
            (d["resident"], d["message"])
            for d in scenario_donnees["demandes"]
        ]

        return cls(
            nom=scenario_donnees["nom"],
            carte=carte,
            armoire=armoire,
            demandes=demandes,
        )

    def __str__(self):
        strng = f"Scénario : {self.nom}\n"
        strng += f"Carte : {self.carte.dimensions}\n"
        strng += f"Nombre de demandes : {len(self.demandes)}\n"
        return strng