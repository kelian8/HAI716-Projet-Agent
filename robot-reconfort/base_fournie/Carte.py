import reconfort_io as rio

class Carte:

    grille = 0
    armoire_pos = 0
    dico_pos = 0
    #residents = dictionnaire{id -> (nom,pos)}
    residents = 0 

    #Objectif de l'intialisation : désirialiser le fichier donné au constructeur
    def __init__(self,chemin):
        carte_donnees = rio.charger_carte(chemin)
        self.grille = carte_donnees.get("grille")
        self.armoire_pos = carte_donnees.get("armoire")

    def __str__(self):
        strng = "Données de la carte : \n"
        #strng += "grille : " + self.grille + "\n"
        strgn += "position de l'armoire" + self.armoire_pos + "\n"
        return strgn