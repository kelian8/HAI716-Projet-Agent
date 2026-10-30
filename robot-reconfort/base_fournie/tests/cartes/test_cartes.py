from pathlib import Path

import pytest

from reconfort_io import charger_carte, ErreurFichier
from Exceptions import ErreurFormatJSON

DOSSIER = Path(__file__).parent

# (fichier JSON, regex cherchée dans le message d'erreur)
CAS_INVALIDES = [
    # Dimensions
    ("dimensions_absentes.json",          "Dimensions introuvables"),
    ("dimensions_sans_hauteur.json",      "Dimensions invalides"),
    # Grille
    ("grille_absente.json",               "Grille introuvable"),
    ("grille_non_rectangulaire.json",     "Grille non rectangulaire"),
    ("grille_dimensions_incoherentes.json", "ne respectent pas les dimensions"),
    # Départ du robot
    ("depart_absent.json",                "Départ du robot introuvable"),
    ("depart_3_coordonnees.json",         "Position du robot non conforme"),
    ("depart_hors_carte.json",            "point de départ du robot"),
    # Armoire
    ("armoire_absente.json",              "Armoire introuvable"),
    ("armoire_sans_position.json",        "Position de l'armoire introuvable"),
    ("armoire_3_coordonnees.json",        "Position de l'armoire non conforme"),
    ("armoire_hors_carte.json",           "position de l'armoire n'est pas dans la carte"),
    # Dictionnaire
    ("dictionnaire_absent.json",          "Dictionnaire introuvable"),
    ("dictionnaire_sans_position.json",   "Position du dictionnaire introuvable"),
    ("dictionnaire_3_coordonnees.json",   "Position du dictionnaire non conforme"),
    ("dictionnaire_hors_carte.json",      "position du dictionnaire n'est pas dans la carte"),
    # Résidents
    ("residents_absents.json",            "Résidents introuvables"),
    ("resident_sans_nom.json",            "Un résident est mal formatté"),
    ("resident_3_coordonnees.json",       "Position du résident .* non conforme"),
    ("resident_hors_carte.json",          "résident .* pas dans la carte"),
    ("residents_id_en_double.json",       "en doublon"),
]


def test_carte_valide():
    """Le fichier valide se charge sans exception et donne les bonnes valeurs."""
    carte = charger_carte(DOSSIER / "valide.json")
    assert carte.dimensions == (9, 13)
    assert carte.depart_robot == (6, 1)
    assert carte.armoire_pos == (6, 4)
    assert carte.dico_pos == (7, 6)
    assert carte.residents == [{
      "id": "R1",
      "nom": "Camille",
      "position": [
        6,
        11
      ]
    },
    {
      "id": "R2",
      "nom": "Hugo",
      "position": [
        3,
        3
      ]
    }]


@pytest.mark.parametrize("fichier, message", CAS_INVALIDES)
def test_carte_invalide(fichier, message):
    """Chaque fichier invalide lève ErreurFormatJSON avec le bon message."""
    with pytest.raises(ErreurFormatJSON, match=message):
        charger_carte(DOSSIER / fichier)


# --- Cas gérés par _lire_json ---

def test_fichier_absent(tmp_path):
    with pytest.raises(ErreurFichier):
        charger_carte(tmp_path / "nexiste_pas.json")


def test_json_syntaxe_invalide():
    with pytest.raises(ErreurFichier):
        charger_carte(DOSSIER / "json_syntaxe_invalide.json")


def test_format_inattendu():
    with pytest.raises(ErreurFichier):
        charger_carte(DOSSIER / "format_inattendu.json")


def test_version_inattendue():
    with pytest.raises(ErreurFichier):
        charger_carte(DOSSIER / "version_inattendue.json")


def test_pas_utf8(tmp_path):
    f = tmp_path / "latin1.json"
    f.write_bytes('{"nom": "é"}'.encode("latin-1"))
    with pytest.raises(ErreurFichier):
        charger_carte(f)


def test_aucun_fichier_oublie():
    """Garde-fou : chaque JSON du dossier est valide.json ou listé ci-dessus."""
    attendus = {f for f, _ in CAS_INVALIDES} | {
        "valide.json", "json_syntaxe_invalide.json",
        "format_inattendu.json", "version_inattendue.json",
    }
    assert {p.name for p in DOSSIER.glob("*.json")} == attendus