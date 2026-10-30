from pathlib import Path

from .Robot import Robot
from Scenario import Scenario
import reconfort_io as rio


class Simulation:

    def __init__(self, scenario, dictionnaire:dict[str,tuple[str,str]],chemin_trace:str|Path):
        self.robot = Robot(self)
        self.scenario:Scenario = scenario
        self.dictionnaire = dictionnaire
        self.trace = rio.Trace(self.scenario.nom_carte,self.scenario.nom,("BAEZA kelian", "HOURMAND Théo"))
        self.chemin_trace = chemin_trace
        self.pas:int = 0

    def get_dico(self):
        return self.dictionnaire

    def get_carte(self):
        return self.scenario.carte

    def get_armoire(self):
        return self.scenario.armoire

    def get_demandes(self):
        return self.scenario.demandes

    def get_next_demande(self):
        demandes = self.get_demandes()
        if len(demandes) != 0:
            return demandes.pop(0)
        else :
            return None

    def get_robot_depart(self):
        return self.scenario.carte.depart_robot

    def get_casier_depart(self):
        return self.scenario.armoire.casier_depart

    def get_carte_size(self):
        return (self.scenario.carte.dimensions[0],self.scenario.carte.dimensions[1])

    def get_armoire_pos(self):
        return self.scenario.carte.get_position("armoire")

    def get_dico_pos(self):
        return self.scenario.carte.get_position("dictionnaire")

    def get_resident_pos(self, id:str):
        return self.scenario.carte.get_position("resident",id)

    def get_residents(self):
        return self.scenario.carte.residents

    def get_symbole(self, ligne, colonne):
        return self.scenario.carte.grille[ligne][colonne]


    def simulation(self):
        running = True
        while(running):
            self.robot.simulation_step()
            print(f"Pas de simulation n°{self.pas}")
            print(f"Etat courant du robot : {self.robot.etat}")
            print(f"Grille du robot :")
            print(self.robot.grille_connue)
            print("==============================")
            entree = input("Appuyez sur entrée pour passer au pas suivant," \
            "bien écrivez 'q' pour arrêter la simulation et enregistrer la trace")
            if entree.strip().lower() == 'q':
                running = False
            self.pas += 1

        self.trace.ecrire(self.chemin_trace)
