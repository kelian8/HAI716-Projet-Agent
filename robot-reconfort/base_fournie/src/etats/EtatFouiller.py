from Etat import Etat
from Robot import *

class EtatFouiller(Etat):

    def enter(self):
        print("Le robot fouille dans l'armoire.")


    def exit(self):
        
        print("Le robot a fini de fouiller dans l'armoire.")

    def simulation_step(self):
        pass#TODO