from Etat import Etat
from Robot import *

class EtatNavigationDico(Etat):

    def enter(self):
        print("Le robot commence à se déplacer vers l'armoire.")


    def exit(self):
        
        print("Le robot quitte l'état de navigation vers l'armoire.")

    def simulation_step(self):
        pass#TODO