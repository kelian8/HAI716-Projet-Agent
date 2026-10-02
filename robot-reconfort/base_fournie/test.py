import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from Scenario import Scenario
from Carte import Carte
import reconfort_io as rio


def main():
    print("hello world")
    s:Scenario = rio.charger_scenario("cartes/scenario_01.json")
    d = rio.charger_dictionnaire("donnees/dictionnaire.json")
    print(s)
    print(d)

if __name__ == "__main__":
    main()