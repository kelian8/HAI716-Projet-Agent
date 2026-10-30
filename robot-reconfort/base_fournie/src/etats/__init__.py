from .etat import Etat
from .EtatInit import EtatInit
from .EtatAttente import EtatAttente
from .EtatNavigationDico import EtatNavigationDico
from .EtatNavigationArm import EtatNavigationArm
from .EtatFouiller import EtatFouiller
from .EtatNavigationRes import EtatNavigationRes


def creer_etats(robot) -> dict[str, Etat]:
    """Instancie chaque état une seule fois.

    Returns:
        Dictionnaire nom d'état -> instance correspondante.
    """
    etats = {
        "EtatInit" : EtatInit(robot),
        "EtatAttente" : EtatAttente(robot),
        "EtatNavigationDico" : EtatNavigationDico(robot),
        "EtatNavigationArm" : EtatNavigationArm(robot),
        "EtatFouiller" : EtatFouiller(robot),
        "EtatNavigationRes" : EtatNavigationRes(robot),
    }
    return etats