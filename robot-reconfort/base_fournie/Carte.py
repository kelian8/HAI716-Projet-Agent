import reconfort_io as rio

class Carte:

    def __init__(self, dimensions, grille, depart_robot, armoire_pos, dico_pos, residents):
        self.dimensions = dimensions
        self.grille = grille
        self.depart_robot = depart_robot
        self.armoire_pos = armoire_pos
        self.dico_pos = dico_pos
        self.residents = residents

    @classmethod
    def _from_json(cls,chemin):
        """ Fonction qui vérifie la validité d'un fichier puis le charge en tant que Carte
        Args : 
            chemin : Chemin du fichier à charger
        
        Returns : 
            une instance de la classe Carte représentant la carte chargée
            
        Raises :
            TODO"""
        carte_donnees = rio.charger_carte(chemin)

        residents = {}
        for r in carte_donnees["residents"]:
            residents[r["id"]] = (r["nom"],tuple(r["position"]))

        return cls(
            dimensions = (carte_donnees["dimensions"]["hauteur"],carte_donnees["dimensions"]["largeur"]),
            grille = carte_donnees["grille"],
            depart_robot = tuple(carte_donnees["depart_robot"]),
            armoire_pos = tuple(carte_donnees["armoire"]["position"]),
            dico_pos = tuple(carte_donnees["dictionnaire"]["position"]),
            residents = residents
        )

    