from Etat import Etat
from Robot import *
from Carte import *

class EtatNavigationDico(Etat):

    def enter(self):
        print("Le robot commence à se déplacer vers le dico.")


    def exit(self):
        print("Le robot quitte l'état de navigation vers le dico.")

    def simulation_step(self):
        arrive=False
        print("le robot se deplace vers le dictionnaire")
        if not self.robot.est_adjacent(self.robot.carte.get_position("dictionnaire")): #verifie si le robot est sur une case adjacente
                                                                                        #au dico
            arrive = self.robot.naviguer_vers(self.robot.carte.get_position("dictionnaire"))#fait la naviguation vers le dico 
        else:
            arrive=True


        if arrive:
            print("le robot est bien arrivé au dictionnaire.")
            self.robot.changerEtat(XXXXXXXXXXX)
