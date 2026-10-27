from .Etat import Etat
from .EtatInit import EtatInit
from .Attente import Attente
from .NavigationDictionnaire import NavigationDictionnaire
from .NavigationArmoire import NavigationArmoire
from .FouillerArmoire import FouillerArmoire
from .NavigationResident import NavigationResident


def creer_etats(robot) -> dict[str, Etat]:
    """Instancie chaque état une seule fois.

    Returns:
        Dictionnaire nom d'état -> instance correspondante.
    """
    etats = {
        "EtatInit" : EtatInit(robot)
        "EtatAttente" : EtatAttente(robot),
        "EtatNavigationDico" : EtatNavigationDico(robot),
        "EtatNavigationArm" : EtatNavigationArm(robot),
        "EtatFouiller" : EtatFouiller(robot),
        "EtatNavigationRes" : EtatNavigationRes(robot),
    }
    return etats