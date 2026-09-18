import reconfort_io as rio
import Carte as C

class Scenario:
    carte = 0
    armoire = 0
    demandes = 0

    def __init__(self):
        self.carte = C.Carte("cartes/appartement_01.json")
        print(self.carte.__str__())