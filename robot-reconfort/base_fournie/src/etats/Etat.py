from abc import ABC, abstractmethod
from Robot import Robot


class Etat(ABC):
    Robot : robot


    def __init__(self,robot:Robot):
        self.robot = robot

    @abstractmethod
    def enter(self):
        """Méthode appelée lors de l'entrée dans un état (initialisations)"""
        pass

    @abstractmethod
    def exit(self):
        """Méthode appelée lors de la sortie d'un état"""
        pass

    @abstractmethod
    def simulation_step(self):
        """Méthode appelée à chaque pas de simulation"""
        pass