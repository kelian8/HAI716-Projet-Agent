from Carte import *


class Robot:

    position : tuple
    carte : Carte
    #dictionnaire de dictionnaire key1 = emotion key1.x = intensité et valeur = liste dposition du ou des casier dans l'armoire 
    #ne sert pas a grand chose pour l'instant si ce n'est savoir si un casier est eventuellement vide et si c'est le cas et qu'on a besoin de l'objet 
    #correspondant, nous irons a un casier ayant uneemotion/intensite proche de celle recherchée initialement
    armoire_connue : dict
    objet_tenu : str | None 
    current_demande : dict |None #demande qu'on traite actuellement
    etat : xxx #etat actuel du robot (recherche x, cherche dans armoire, etc )

    def __init__(self,carte):
        self.position = carte.depart_robot
        
        #la carte donnée au robot lors de son initialisation dans "simulation", est une carte creer par simulation dont la grille a été remplacxe par une gerille
        #"vierge" a l'execption des residents, l'armoire, et le dico 
        self.carte = carte
        self.armoire_connue= {}
        self.objet_tenu=None
        self.current_demande = None
        self.etat = xxx #a remplacer 

        
    """
        inutile mais on garde au cas ou 
        [["." for j in range(taillecarte[0])] for i in range(taillecarte[1])]
    
        #boucle pour rentrer les bordures
        for j in carte.grille:

            #pour la bordure haute et basse
            if j==0 or j==taillecarte[0]:
                for i in range(0,taillecarte[1]):
                    carte[j][i]="#"

            #pour la bordure droite et gauche        
            elif i==0 or i==taillecarte[1]:
                carte[j][i]="#"

        #pour la position des residents
        for k in carte.residents : 
            pass
"""

