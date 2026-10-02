from abc import ABC, abstractmethod

class Etat(ABC):

    def __init__(self,robot:Robot):
        self.robot = robot

    @abstractmethod
    def enter():
        """Méthode appelée lors de l'entrée dans un état (initialisations)"""
        pass

    @abstractmethod
    def exit():
        """Méthode appelée lors de la sortie d'un état"""
        pass

    @abstractmethod
    def simulation_step():
        """Méthode appelée à chaque pas de simulation"""
        pass