from Carte import Carte
from Armoire import Armoire


class Scenario:
    def __init__(self, nom:str, carte:Carte, armoire:Armoire, demandes:list[dict[str,any]]):
        self.nom = nom
        self.carte = carte
        self.armoire = armoire
        self.demandes = demandes


    def __str__(self):
        strng = f"Scénario : {self.nom}\n"
        strng += f"Carte : {self.carte.dimensions}\n"
        strng += f"Nombre de demandes : {len(self.demandes)}\n"
        return strng