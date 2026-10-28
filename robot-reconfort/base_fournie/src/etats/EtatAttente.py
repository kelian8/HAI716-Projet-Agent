from Etat import Etat

class EtatAttente(Etat):

    demande: str | None
    def enter(self):
        print("Le robot entre en état d'attente.")

    def exit(self):
        self.robot.current_demande = self.demande
        print("Le robot quitte l'état d'attente.")

    def simulation_step(self):
        print("Le robot attend une demande.")
        #while self.robot.current_demande == None :
        #    print("en attente d'une demande")
        #Selon moi on ne met pas de while parce que sinon ça prend le dessus sur la simulation
        demande = self.robot.simulation.get_next_demande()
        self.robot.parent.trace.ajouter_pas(
            demande,
            self.robot.position,
            self.robot.position_armoire(),
            "ATTENDRE",

        )
        if (demande != None):
            self.robot.changerEtat("EtatNavigationDico")




