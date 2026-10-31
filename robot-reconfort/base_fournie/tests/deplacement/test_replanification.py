"""
pour ce test de replanification de chemin on utilise l'etat de navigation vers l'armoire comme on aurait pu utiliser
les autres etats de navigations car ils fonctionnent avec la meme logique.
"""

from unittest.mock import Mock

from etats.EtatNavigationArm import EtatNavigationArm


class FauxRobot:
    DIRECTIONS = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "O": (0, -1)
    }

    def __init__(self):
        self.position = (0, 0)
        self.position_armoire = (0, 0)
        self.armoire_pos = (1, 1)

        self.current_demande = None

        self.grille_connue = [
            [".", ".", "."],
            [".", ".", "."],
            [".", ".", "."]
        ]

        self.parent = Mock()

        self.nombre_calculs = 0
        self.directions_tentees = []

    def est_adjacent(self, position):
        return False

    def percevoir_voisins(self):
        return {}

    def mettre_a_jour_grille_connue(self, perceptions):
        pass

    def avancer(self, direction):
        self.directions_tentees.append(direction)
        return False  # Simule un obstacle découvert

    def calculer_chemin(self, destinations):
        self.nombre_calculs += 1

        if self.nombre_calculs == 1:
            return [(0, 0), (0, 1), (0, 2)]

        return [(0, 0), (1, 0), (1, 1)]



def test_replanification_apres_obstacle():
    robot = FauxRobot()#on creer un "faux robot" 
    etat = EtatNavigationArm(robot)

    #on evite de reutiliser une ancienne liste de destinations
    etat.destinations = []

    #l'etat calcule son premier chemin.
    etat.enter()

    #les chemins qu'on va comparer
    ancien_chemin = [(0, 0), (0, 1), (0, 2)]
    nouveau_chemin = [(0, 0), (1, 0), (1, 1)]

    #on verifie que "l'ancien chemin" est bien le chemin actuel
    assert etat.chemin == ancien_chemin

    #le robot tente d'avancer, mais il rencontre un obstacle donc replanifie
    etat.simulation_step()

    #on verifie bien que le chemin replanifié est bien celui qu'on avait prevu
    assert robot.directions_tentees == ["E"]
    assert robot.nombre_calculs == 2
    assert etat.chemin == nouveau_chemin