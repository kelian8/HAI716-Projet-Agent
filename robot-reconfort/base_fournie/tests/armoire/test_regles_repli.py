
from unittest.mock import Mock

from etats.EtatFouiller import EtatFouiller
from Armoire import Armoire


def creer_robot(emotion, intensite, depart=(1, 0)):
    robot = Mock()

    robot.emotion_intensite = (emotion, intensite)
    robot.position_armoire = depart
    robot.armoire_connue = {}
    robot.objet_tenu = None
    robot.repli = "aucun"

    robot.parent.get_armoire.return_value = Armoire(depart)

    return robot


def test_casier_exact_garni():
    robot = creer_robot("surprise", "forte")

    armoire = robot.parent.get_armoire.return_value
    armoire.add_objet(2, 3, "telephone")

    robot.armoire_connue[(2, 3)] = "telephone"
    robot.position_armoire = (2, 3)

    robot.prendre.return_value = True

    etat = EtatFouiller(robot)
    etat.enter()
    etat.simulation_step()

    assert robot.prendre.called
    assert robot.repli == "aucun"
    robot.changer_etat.assert_called_once_with("EtatNavigationRes")



def test_casier_exact_vide_repli_intensite():
    robot = creer_robot("surprise", "forte")

    armoire = robot.parent.get_armoire.return_value
    armoire.add_objet(1, 3, "telephone")

    #on admet que le robot a connaissance du casier (sinon condition pas validee quand on veut prendre l'objet) 
    #on est oblige de le faire manuellement car cest un mock
    robot.armoire_connue[(1, 3)] = "telephone"

    #on sait deja que le casier exact est vide
    robot.armoire_connue[(2, 3)] = None

    #on place le selecteur devant le casier
    robot.position_armoire = (2, 3)

    robot.prendre.return_value = True

    etat = EtatFouiller(robot)
    etat.enter()

    #on execute 
    etat.simulation_step()

    #on fait bouger manuelement le robot
    robot.position_armoire = (1, 3)

    #on reexecute
    etat.simulation_step()

    #on teste si le robot va bien vers le bon casier
    assert robot.repli == "intensite" or robot.prendre.called





def test_colonne_vide_repli_voisine():
    robot = creer_robot("surprise", "forte")

    #on connaît les trois casiers de la colonne surprise :
    # et ils sont tous vides.
    robot.armoire_connue[(2, 3)] = None
    robot.armoire_connue[(1, 3)] = None
    robot.armoire_connue[(0, 3)] = None

    #le casier voisin contient un telephone
    armoire = robot.parent.get_armoire.return_value
    armoire.add_objet(2, 4, "telephone")
    robot.armoire_connue[(2, 4)] = "telephone"

    #on place alors le selecteur devant le casier exact
    robot.position_armoire = (2, 3)

    robot.prendre.return_value = True

    etat = EtatFouiller(robot)
    etat.enter()

    #on passe les trois casiers vides grace au pas de simulation
    etat.simulation_step()
    etat.simulation_step()
    etat.simulation_step()

    #on simule l'arrivée devant le casier voisin
    robot.position_armoire = (2, 4)

    etat.simulation_step()

    assert robot.prendre.called
    assert robot.repli == "voisine_1"
    robot.changer_etat.assert_called_once_with("EtatNavigationRes")



def test_aucun_casier_disponible():
    robot = creer_robot("surprise", "forte")

    #tous les candidats sont connus et vides
    etat = EtatFouiller(robot)
    etat.enter()

    for cible in etat.candidats:
        robot.armoire_connue[cible] = None

    robot.current_demande = None

    #on fait un pas de simulation pour chaque candidats
    for _ in range(len(etat.candidats)):
        etat.simulation_step()

    assert etat.indice_candidat == len(etat.candidats)
    robot.prendre.assert_not_called()