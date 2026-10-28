from Etat import Etat

class EtatInit(Etat):

    def enter(self):
        pass

    def exit(self):
        pass

    def simulation_step(self):
        print("Mise en route du robot")
        self.robot.changer_etat("EtatAttente")
