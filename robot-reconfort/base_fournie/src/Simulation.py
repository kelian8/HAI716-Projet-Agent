from pathlib import Path

from etats import EtatFouiller

from .Robot import Robot
from Scenario import Scenario
import reconfort_io as rio

import os

def effacer_ecran() -> None:
    """Efface le contenu du terminal."""
    os.system("cls" if os.name == "nt" else "clear")


class Simulation:

    def __init__(self, scenario, dictionnaire:dict[str,tuple[str,str]],chemin_trace:str|Path):
        self.scenario:Scenario = scenario
        self.dictionnaire = dictionnaire
        self.trace = rio.Trace(self.scenario.nom_carte,self.scenario.nom,("BAEZA kelian", "HOURMAND Théo"))
        self.chemin_trace = chemin_trace
        self.pas:int = 0
        self.robot = Robot(self)

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
            effacer_ecran()
            self.robot.simulation_step()
            print(f"Pas de simulation n°{self.pas}")
            print(f"Etat courant du robot : {self.robot.etat}")
            print("position du robot : " + str(self.robot.position))
            if (isinstance(self.robot.etat,EtatFouiller)):
                print("Armoire du robot : ")
                self.print_armoire(self.robot.armoire_connue,self.robot.position_armoire)
            else :
                print("Grille du robot :")
                self.print_grille(self.robot.grille_connue)
            print("==============================")
            entree = input("Appuyez sur entrée pour passer au pas suivant," \
            "ou bien écrivez 'q' pour arrêter la simulation et enregistrer la trace :")
            if entree.strip().lower() == 'q':
                running = False
            self.pas += 1
            

        self.trace.ecrire(self.chemin_trace)

    def print_grille(self, grille:list[list[str]]):
        for row in range(len(grille)):
            for col in range(len(grille[row])):
                if (row,col) == self.robot.position:
                    print("R",end="")
                else : 
                    print(grille[row][col],end="")
            print()

    def print_armoire(self, armoire:dict[tuple[int,int],str],pos:tuple[int,int]):
        for row in range(3):
            for col in range(8):
                if (row,col) == pos :
                    print("[",end="")
                if (row,col) in armoire:
                    if armoire[(row,col)] == None:
                        print("Vide",end="")
                    else :
                        print(armoire[(row,col)],end="")
                else :
                    print("Vide",end="")
                if (row,col) == pos :
                    print("]",end="")
            print()
