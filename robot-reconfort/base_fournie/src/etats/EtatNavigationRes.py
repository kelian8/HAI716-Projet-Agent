from Etat import Etat
from Robot import *

class EtatNavigationRes(Etat):

    def enter(self):
        print("Le robot commence à se déplacer vers le résident.")


    def exit(self):
        
        print("Le robot quitte l'état de navigation vers le résident.")

    def simulation_step(self):
        pass#TODO