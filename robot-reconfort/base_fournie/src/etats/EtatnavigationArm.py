from Etat import Etat
from Robot import *

class EtatNavigationArm(Etat):

    def enter(self):
        print("Le robot commence à se déplacer vers l'armoire.")


    def exit(self):
        
        print("Le robot quitte l'état de navigation vers l'armoire.")

    def simulation_step(self):
        arrive=False
        print("le robot se deplace vers l'armoire")
        if not self.robot.est_adjacent(self.robot.armoire_pos): #verifie si le robot est sur une case adjacente
                                                                                        #à l'armoire
            arrive = self.robot.naviguer_vers(self.robot.armoire_pos)#fait la naviguation vers l'armoire 
        else:
            arrive=True


        if arrive:
            print("le robot est bien arrivé à l'armoire.")
            self.robot.changer_etat("EtatFouiller")