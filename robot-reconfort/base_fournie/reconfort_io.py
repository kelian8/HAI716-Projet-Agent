"""
Base de code fournie -- projet "Robot de reconfort".

Ce module fait DEUX choses, et rien d'autre :

  1. lire les quatre fichiers d'entree (carte, dictionnaire, armoire,
     scenario) ;
  2. construire et exporter le fichier de trace attendu a la sortie.

Tout le reste du projet -- perception, carte mentale, planification de
chemin, consultation du dictionnaire, fouille de l'armoire, boucle de
decision -- est a votre charge. Ne cherchez pas ces fonctions ici : elles
n'y sont pas, et c'est volontaire.

Vous avez le droit de modifier ce fichier. Vous avez surtout le devoir de
le comprendre : les verifications faites ici sont minimales (voir la
section "Ce qui n'est PAS verifie" plus bas), et les validations
manquantes font partie du travail demande.

Python 3.9+. Aucune dependance externe.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

"""Import des classes pour chargement"""
from Exceptions import ErreurFormatJSON
from Carte import Carte

__all__ = [
    "ErreurFichier",
    "charger_carte",
    "charger_dictionnaire",
    "charger_armoire",
    "charger_scenario",
    "normaliser",
    "Trace",
]

VERSION_ATTENDUE = 1


class ErreurFichier(Exception):
    """Fichier d'entree absent, illisible, ou d'un type inattendu."""


# ---------------------------------------------------------------------------
# Lecture
# ---------------------------------------------------------------------------

def _lire_json(chemin: str | Path, format_attendu: str) -> Dict[str, Any]:
    """Lit un fichier JSON UTF-8 et verifie son en-tete.

    Ce qui EST verifie ici :
      - le fichier existe et se lit en UTF-8 ;
      - son contenu est du JSON valide ;
      - la racine est un objet ;
      - les champs "format" et "version" sont presents et corrects.

    Ce qui n'est PAS verifie (a vous de le faire, enonce section 5.6) :
      - la presence et le type de chacun des autres champs ;
      - la coherence des donnees (grille rectangulaire, positions dans les
        bornes, resident pose sur un mur, casier hors de l'armoire,
        emotion inconnue, resident cite par un scenario mais absent de la
        carte...).
    """
    chemin = Path(chemin)
    try:
        texte = chemin.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ErreurFichier(f"fichier introuvable : {chemin}") from None
    except UnicodeDecodeError as err:
        raise ErreurFichier(
            f"{chemin} n'est pas encode en UTF-8 (octet {err.start})"
        ) from None
    except OSError as err:
        raise ErreurFichier(f"{chemin} illisible : {err}") from None

    try:
        donnees = json.loads(texte)
    except json.JSONDecodeError as err:
        raise ErreurFichier(
            f"{chemin} n'est pas un JSON valide : {err.msg} "
            f"(ligne {err.lineno}, colonne {err.colno})"
        ) from None

    if not isinstance(donnees, dict):
        raise ErreurFichier(
            f"{chemin} : la racine doit etre un objet JSON, "
            f"pas {type(donnees).__name__}"
        )

    format_trouve = donnees.get("format")
    if format_trouve != format_attendu:
        raise ErreurFichier(
            f"{chemin} : format attendu '{format_attendu}', "
            f"trouve {format_trouve!r}"
        )

    version = donnees.get("version")
    if version != VERSION_ATTENDUE:
        raise ErreurFichier(
            f"{chemin} : version {VERSION_ATTENDUE} attendue, trouve {version!r}"
        )

    return donnees

def position_valide(position:(int,int), dimensions:(int,int))->bool:
    """Vérification de position dans la grille
    Args :
        position : paire d'entier représentant la position à vérifier
        dimensions : la taille de la carte
        
    Returns :
        True ssi position est valide (c'est à dire chaque coordonnée est comprise entre 0 et la taille de la carte)"""
    return 0 < position[0] < dimensions[0] and 0 < position[1] < dimensions[1]


def charger_carte(chemin: str | Path) -> Carte:
    """Charge un fichier carte. Voir l'enonce, section 5.1.
    Args :
        chemin : Chemin du fichier JSON à charger
    
    Returns :
        Une instance de la classe Carte pour représenter la carte chargée

    Raises :
        ErreurFormatJson : si le JSON n'est pas formatté correctement
        """

    values : Dict[str, Any] = _lire_json(chemin,"robot-reconfort/carte")

    #Dimensions
    if "dimensions" not in values :
        raise ErreurFormatJSON("Dimensions introuvables", chemin)
    if "hauteur" not in values["dimensions"] or "largeur" not in values["dimensions"] :
        raise ErreurFormatJSON("Dimensions invalides")
    dimensions = (values["dimensions"]["hauteur"],values["dimensions"]["largeur"])

    #Grille :
    if "grille" not in values:
        raise ErreurFormatJson("Grille introuvable : ", chemin)
    
    grille = values["grille"]
    for row in grille :
        if len(row) != len(grille[0]) :
            raise ErreurFormatJSON("Grille non rectangulaire", chemin)
    
    if len(grille) != dimensions[0] or any(len(ligne) != dimensions[1] for ligne in grille):
        raise ErreurFormatJSON("Les dimensions de la grille ne respectent pas les dimensions données", chemin)


    #Depart robot :
    if "depart_robot" not in values:
        raise ErreurFormatJson("Départ du robot introuvable : ", chemin)
    depart_robot:tuple = tuple(values["depart_robot"])
    if len(depart_robot) != 2 :
        raise ErreurFormatJSON("Position du robot non conforme", chemin)
    if not position_valide(depart_robot,dimensions):
        raise ErreurFormatJSON("Le point de départ du robot n'est pas dans la carte")

    #Position de l'armoire
    if "armoire" not in values:
        raise ErreurFormatJson("Armoire introuvable : ", chemin)
    if "position" not in values["armoire"]:
        raise ErreurFormatJson("Position de l'armoire introuvable : ", chemin)
    armoire_pos:tuple = tuple(values["armoire"]["position"])
    if len(armoire_pos) != 2 :
        raise ErreurFormatJSON("Position de l'armoire non conforme", chemin)
    if not position_valide(armoire_pos,dimensions):
        raise ErreurFormatJSON("La position de l'armoire n'est pas dans la carte", chemin)

    #Position du dictionnaire
    if "dictionnaire" not in values:
        raise ErreurFormatJson("Dictionnaire introuvable : ", chemin)
    if "position" not in values["dictionnaire"]:
        raise ErreurFormatJson("Position du dictionnaire introuvable : ", chemin)
    dico_pos:tuple = tuple(values["dictionnaire"]["position"])
    if len(dico_pos) != 2 :
        raise ErreurFormatJSON("Position du dictionnaire non conforme", chemin)
    if not position_valide(dico_pos,dimensions):
        raise ErreurFormatJSON("La position de l'armoire n'est pas dans la carte", chemin)


    #Résidents
    if "residents" not in values:
        raise ErreurFormatJSON("Résidents introuvables", chemin)
    residents = {}
    for r in values["residents"]:
        if "id" not in r or "nom" not in r or "position" not in r:
            raise ErreurFormatJSON("Un résident est mal formatté",chemin)
        r_pos:tuple = tuple(r["position"])
        if len(r_pos) != 2 :
            raise ErreurFormatJSON("Position du résident "+ r["nom"] + " non conforme", chemin)
        if not position_valide(r_pos,dimensions):
            raise ErreurFormatJSON("La position du résident "+ r["nom"] + " pas dans la carte", chemin)
        residents[r["id"]] = (r["nom"],r_pos)

    return Carte(
        dimensions = dimensions,
        grille = grille,
        depart_robot = depart_robot,
        armoire_pos = armoire_pos,
        dico_pos = dico_pos,
        residents = residents
    )



    return _lire_json(chemin, "robot-reconfort/carte")


def charger_dictionnaire(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier dictionnaire. Voir l'enonce, section 5.2."""
    return _lire_json(chemin, "robot-reconfort/dictionnaire")


def charger_armoire(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier armoire. Voir l'enonce, section 5.3."""
    return _lire_json(chemin, "robot-reconfort/armoire")


def charger_scenario(chemin: str | Path) -> Dict[str, Any]:
    """Charge un fichier scenario. Voir l'enonce, section 5.1.
    Args :
        chemin : Chemin du fichier JSON à charger
    
    Returns :
        Une instance de la classe Carte pour représenter la carte chargée

    Raises :
        ErreurFormatJson : si le JSON n'est pas formatté correctement
        """

    values :Dict[str, Any] = _lire_json(chemin, "robot-reconfort/scenario")

    # La carte est désérialisée à partir de son propre fichier,
    # construit à partir du nom donné dans le scénario
    chemin_carte = "cartes/" + scenario_donnees["carte"] + ".json"
    carte = charger_carte(chemin_carte)

    # Idem à terme pour l'armoire : le scénario ne stocke qu'un nom,
    # on va chercher le fichier correspondant et on désérialise
    # chemin_armoire = "armoires/" + scenario_donnees["armoire"] + ".json"
    # armoire = Armoire._from_json(chemin_armoire)
    armoire = scenario_donnees["armoire"]  # provisoire : juste le nom en string pour l'instant

    demandes = [
        (d["resident"], d["message"])
        for d in scenario_donnees["demandes"]
    ]

    return cls(
        nom=scenario_donnees["nom"],
        carte=carte,
        armoire=armoire,
        demandes=demandes,
    )


# ---------------------------------------------------------------------------
# Normalisation des messages
# ---------------------------------------------------------------------------

def normaliser(texte: str) -> List[str]:
    """Decoupe un message en mots comparables au dictionnaire.

    Minuscules, accents retires, decoupage sur tout ce qui n'est pas une
    lettre. C'est exactement la regle de l'enonce, section 6.1 ;
    reimplementez-la vous-meme si vous travaillez dans un autre langage.

        >>> normaliser("Je suis TERRIFIEE, vraiment !")
        ['je', 'suis', 'terrifiee', 'vraiment']
    """
    decompose = unicodedata.normalize("NFD", texte.lower())
    sans_accents = "".join(
        c for c in decompose if unicodedata.category(c) != "Mn"
    )
    mots: List[str] = []
    courant: List[str] = []
    for caractere in sans_accents:
        if caractere.isalpha():
            courant.append(caractere)
        elif courant:
            mots.append("".join(courant))
            courant = []
    if courant:
        mots.append("".join(courant))
    return mots


# ---------------------------------------------------------------------------
# Ecriture de la trace
# ---------------------------------------------------------------------------

ACTIONS = ("AVANCER", "CONSULTER", "CHERCHER", "PRENDRE", "DONNER", "ATTENDRE")
DIRECTIONS = ("N", "S", "E", "O")
REPLIS = ("aucun", "intensite", "voisine_1", "voisine_2")


class Trace:
    """Accumule les pas et les livraisons, puis ecrit le fichier de sortie.

    Utilisation typique :

        trace = Trace(nom_carte="appartement_01",
                      nom_scenario="scenario_01",
                      equipe=["Dupont", "Martin"])
        ...
        trace.ajouter_pas(demande=1, position=(6, 1), casier=(1, 0),
                          action="AVANCER", argument="E",
                          perception={"N": "libre", "S": "mur",
                                      "E": "libre", "O": "mur"})
        ...
        trace.ajouter_livraison(demande=1, resident="R1",
                                emotion="tristesse", intensite="moyenne",
                                casier_choisi=(1, 4), repli="aucun",
                                objet="couverture", succes=True)
        trace.ecrire("sorties/trace_01.json")
    """

    def __init__(
        self,
        nom_carte: str,
        nom_scenario: str,
        equipe: Optional[Sequence[str]] = None,
    ) -> None:
        self.nom_carte = nom_carte
        self.nom_scenario = nom_scenario
        self.equipe: List[str] = list(equipe or [])
        self.pas: List[Dict[str, Any]] = []
        self.livraisons: List[Dict[str, Any]] = []

    # -- pas ---------------------------------------------------------------

    def ajouter_pas(
        self,
        demande: Optional[int],
        position: Sequence[int],
        casier: Sequence[int],
        action: str,
        argument: Optional[str] = None,
        perception: Optional[Dict[str, str]] = None,
        contenu_casier: Optional[str] = None,
        commentaire: Optional[str] = None,
    ) -> None:
        """Enregistre un pas de simulation.

        `position`  : couple (ligne, colonne) du robot AVANT l'action.
        `casier`    : couple (ligne, colonne) du selecteur dans l'armoire,
                      AVANT l'action.
        `perception`: ce que le robot voit depuis sa position, sous la forme
                      d'un dictionnaire des quatre directions vers "mur",
                      "libre", "armoire", "dictionnaire" ou "resident".
        `contenu_casier` : l'objet du casier courant, quand le robot est
                      devant l'armoire et peut donc le voir ; None sinon.
        """
        if action not in ACTIONS:
            raise ValueError(
                f"action inconnue {action!r} (attendu : {', '.join(ACTIONS)})"
            )
        if action in ("AVANCER", "CHERCHER") and argument not in DIRECTIONS:
            raise ValueError(
                f"{action} attend une direction parmi {DIRECTIONS}, "
                f"pas {argument!r}"
            )
        self.pas.append({
            "t": len(self.pas),
            "demande": demande,
            "position": [int(position[0]), int(position[1])],
            "casier": [int(casier[0]), int(casier[1])],
            "action": action,
            "argument": argument,
            "perception": dict(perception) if perception else None,
            "contenu_casier": contenu_casier,
            "commentaire": commentaire,
        })

    # -- livraisons --------------------------------------------------------

    def ajouter_livraison(
        self,
        demande: int,
        resident: str,
        emotion: Optional[str],
        intensite: Optional[str],
        casier_choisi: Optional[Sequence[int]],
        repli: str,
        objet: Optional[str],
        succes: bool,
        motif_echec: Optional[str] = None,
    ) -> None:
        """Enregistre l'issue d'une demande, reussie ou non.

        En cas d'echec, `succes` vaut False et `motif_echec` explique
        pourquoi en une chaine courte (par exemple "resident inaccessible",
        "armoire vide", "emotion indeterminee").
        """
        if repli not in REPLIS:
            raise ValueError(
                f"repli inconnu {repli!r} (attendu : {', '.join(REPLIS)})"
            )
        if not succes and not motif_echec:
            raise ValueError("un echec doit etre accompagne d'un motif_echec")
        self.livraisons.append({
            "demande": int(demande),
            "resident": resident,
            "emotion": emotion,
            "intensite": intensite,
            "casier_choisi": ([int(casier_choisi[0]), int(casier_choisi[1])]
                              if casier_choisi is not None else None),
            "repli": repli,
            "objet": objet,
            "pas_utilises": sum(1 for p in self.pas if p["demande"] == demande),
            "succes": bool(succes),
            "motif_echec": motif_echec,
        })

    # -- export ------------------------------------------------------------

    def en_dictionnaire(self) -> Dict[str, Any]:
        reussies = sum(1 for l in self.livraisons if l["succes"])
        return {
            "format": "robot-reconfort/trace",
            "version": VERSION_ATTENDUE,
            "carte": self.nom_carte,
            "scenario": self.nom_scenario,
            "equipe": self.equipe,
            "pas": self.pas,
            "livraisons": self.livraisons,
            "resume": {
                "demandes": len(self.livraisons),
                "reussies": reussies,
                "echecs": len(self.livraisons) - reussies,
                "pas_total": len(self.pas),
            },
        }

    def ecrire(self, chemin: str | Path) -> Path:
        """Ecrit la trace en JSON UTF-8 indente. Cree le dossier au besoin."""
        chemin = Path(chemin)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(
            json.dumps(self.en_dictionnaire(), ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
        return chemin
