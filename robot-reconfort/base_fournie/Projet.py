import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from src.Simulation import Simulation
import reconfort_io as rio


def main() -> None:
    """Point d'entrée : lit les arguments et lance la simulation."""
    if len(sys.argv) != 4:
        print("Usage : python Projet.py <carte> <scenario> <dossier_donnees> <trace>")
        sys.exit(1)

    #chemin_carte = sys.argv[1] On enlève l'entrée de la carte : elle est dans le scenario
                                #C'est techniquement pareil pour l'armoire : elle est chargée depuis le scenario
    chemin_scenario = sys.argv[1]
    dossier_donnees = sys.argv[2]
    chemin_trace = sys.argv[3]

    scenario = rio.charger_scenario(chemin_scenario,dossier_donnees)
    dictionnaire = rio.charger_dictionnaire(dossier_donnees)

    simulation = Simulation(scenario,dictionnaire,chemin_trace)
    simulation.simulation()


if __name__ == "__main__":
    main()