
from Robot import Robot


def test_chemin_avec_un_obstacle():
    #creation du robot sans passer par le constructeur
    robot = Robot.__new__(Robot)

    #grille connue faite a la main
    robot.grille_connue = [
        [".", ".", "."],
        [".", "#", "."],
        [".", ".", "."]
    ]

    robot.position = (1, 0)
    destination = [(1, 2)]

    chemin = robot.calculer_chemin(destination)

    #en principe le chemin contient 5 position soit 4 deplacement
    assert len(chemin) == 5

    #on verifie le depart et de l'arrivée
    assert chemin[0] == (1, 0)
    assert chemin[-1] == (1, 2)

    #on verifie que le robot ne traverse pas le mur
    for ligne, colonne in chemin:
        assert robot.grille_connue[ligne][colonne] != "#"

    #on verifie que chaque deplacement est adjacent a sa case 
    for i in range(len(chemin) - 1):
        l1, c1 = chemin[i]
        l2, c2 = chemin[i + 1]

        assert abs(l1 - l2) + abs(c1 - c2) == 1


def test_destination_inaccessible():
    robot = Robot.__new__(Robot)

    #grille avec resident enmuré
    robot.position = (1, 0)
    robot.grille_connue = [
        ["#", "#", "#", "#"],
        [".", ".", "P", "#"],
        ["#", "#", "#", "#"]
    ]

    chemin = robot.calculer_chemin([(1, 2)])

    #on verifie que le chemin renvoyé est une liste vide = pas de chemin 
    assert chemin == []