from Etat import Etat
from EtatNavigationDico

class EtatAttente(Etat):

    def enter(self):
        print("Le robot entre en état d'attente.")

    def exit(self):
        print("Le robot quitte l'état d'attente.")

    def simulation_step(self):
        print("Le robot attend une demande.")
        while self.robot.current_demande == None :
            print("en attente d'une demande")
        self.robot.changerEtat(EtatNavigationDico)




