
from unittest.mock import Mock

from etats.EtatNavigationDico import EtatNavigationDico


def creer_etat(message, dictionnaire):
    robot = Mock()
    robot.current_demande = {"message": message}
    robot.parent.dictionnaire = dictionnaire

    return EtatNavigationDico(robot)

#on verifie que le mot est bien reconnu et associé a la bonne emotion
def test_premier_mot_reconnu():
    dictionnaire = {
        "triste": ("tristesse", "moyenne"),
    }

    etat = creer_etat("Je suis vraiment triste", dictionnaire)

    assert etat.consulter() == ("tristesse", "moyenne")

#on verifie que le premier mot est bien reconnu et associé a la bonne emotion meme lorsque 2 mots sont suceptibles d'etre reconnus
def test_premier_mot_reconnu_parmi_deux():
    dictionnaire = {
        "triste": ("tristesse", "moyenne"),
        "peur": ("peur", "forte"),
    }

    etat = creer_etat("Je suis triste et j'ai peur", dictionnaire)

    assert etat.consulter() == ("tristesse", "moyenne")

#on verifie le comportement lorsque qu'aucun mot n'est reconnu
def test_aucun_mot_reconnu():
    dictionnaire = {
        "triste": ("tristesse", "moyenne"),
        "peur": ("peur", "forte"),
    }

    etat = creer_etat("Je vais bien aujourd'hui", dictionnaire)

    assert etat.consulter() is None

#on verifie le comportement lorsque qu'aucune demande n'est en cours
def test_aucune_demande_en_cours():
    robot = Mock()
    robot.current_demande = None

    etat = EtatNavigationDico(robot)

    assert etat.consulter() is None
