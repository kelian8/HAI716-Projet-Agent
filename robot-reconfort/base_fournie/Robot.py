class Robot:

    position
    carte
    armoire_connue
    objet_tenu

    def __init__(self,position,taillecarte, carte, chemin):
        self.position = position
        
        #creer un objet carte pour le robot
        self.carte = Carte(chemin)

        #remplace la grille de l'objet carte par une grille inexplorée
        self.carte.grille = [["." for j in range(taillecarte[0])] for i in range(taillecarte[1])]
        

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
