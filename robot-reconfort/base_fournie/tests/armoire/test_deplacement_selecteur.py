
from unittest.mock import Mock

from Robot import Robot


def creer_robot(position):
    robot = Robot.__new__(Robot)

    robot.position_armoire = position
    robot.position = (0, 0)
    robot.current_demande = None
    robot.armoire_connue = {}

    robot.parent = Mock()
    robot.parent.get_armoire().get_objet.return_value = "telephone"

    return robot


def test_bouclage_est_colonne_7_vers_0():
    robot = creer_robot((1, 7))

    resultat = robot.chercher("E")

    assert resultat is True#on verifie que le deplacement a ete possible
    assert robot.position_armoire == (1, 0)#on verifie que la position du selceteur apres le deplacement est bien celle attendue
    assert robot.armoire_connue[(1, 0)] == "telephone"#et on verifie que le robot a bien mit a jour sa memoire apres son deplacement

#pareil mais dans l'autre sens de la boucle
def test_bouclage_ouest_colonne_0_vers_7():
    robot = creer_robot((1, 0))

    resultat = robot.chercher("O")

    assert resultat is True
    assert robot.position_armoire == (1, 7)
    assert robot.armoire_connue[(1, 7)] == "telephone"



#on teste les deplacements verticaux, il n'y a pas vraiment besoin de commentaire cest quand meme assez clair la 


def test_deplacement_nord_impossible_depuis_ligne_0():
    robot = creer_robot((0, 3))

    resultat = robot.chercher("N")

    assert resultat is False
    assert robot.position_armoire == (0, 3)


def test_deplacement_sud_impossible_depuis_ligne_2():
    robot = creer_robot((2, 3))

    resultat = robot.chercher("S")

    assert resultat is False
    assert robot.position_armoire == (2, 3)



def test_deplacement_nord():
    robot = creer_robot((1, 3))

    resultat = robot.chercher("N")

    assert resultat is True
    assert robot.position_armoire == (0, 3)


def test_deplacement_sud():
    robot = creer_robot((1, 3))

    resultat = robot.chercher("S")

    assert resultat is True
    assert robot.position_armoire == (2, 3)
