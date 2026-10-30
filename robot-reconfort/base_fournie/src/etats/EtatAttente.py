from .etat import Etat

class EtatAttente(Etat):

    def __init__(self, robot):
        super().__init__(robot)
        self.demande: dict | None = None

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
        self.demande = self.robot.parent.get_next_demande()
        
        if (self.demande != None):
            self.robot.parent.trace.ajouter_pas(
                self.demande["numero"],
                self.robot.position,
                self.robot.position_armoire,
                "ATTENDRE",
            )
            print(f"Demande reçu : n° {self.demande["numero"]}, résident : {self.demande["resident"]}, message : {self.demande["message"]}" )
            self.robot.changer_etat("EtatNavigationDico")
        else :
            self.robot.parent.trace.ajouter_pas(
                -1,
                self.robot.position,
                self.robot.position_armoire(),
                "ATTENDRE",
            )

    def __str__(self):
        return "Etat Attente"




