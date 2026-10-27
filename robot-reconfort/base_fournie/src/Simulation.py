import reconfort_io as rio
import Robot

class Simulation:

    robot
    scenario 
    dictionnaire

    def __init__(self, scenario, dictionnaire):
        self.robot = Robot(self)
        self.scenario = scenario
        self.dictionnaire = dictionnaire

    def get_dico():
        return self.dictionnaire

    def get_carte():
        return self.scenario.carte

    def get_armoire():
        return self.scenario.armoire

    def get_demandes():
        return self.scenario.demandes

    def get_next_demande():
        demades = get_demandes()
        if len(demandes) != 0:
            return demandes.pop(0)

    def get_robot_depart():
        return self.scenario.carte.depart_robot

    def get_carte_size():
        return tuple(self.scenario.carte.dimensions["hauteur"],self.scenario.carte.dimensions["largeur"])

    def get_armoire_pos():
        return self.scenario.carte.get_position("armoire")

    def get_dico_pos():
        return self.scenario.carte.get_position("dictionnaire")

    def get_resident_pos(id:str):
        return self.scenario.carte.get_position("resident",id)

    def get_residents():
        return self.scenario.carte.residents

    def get_symbole(ligne, colonne):
        return self.scenario.carte.grille[ligne][colonne]


    def simulation():
        while(1):
            robot.simulation_step()