import Scenario as sc
from Carte import Carte
import reconfort_io as rio


def main():
    print("hello world")
    c:Carte = rio.charger_carte("cartes/appartement_01.json")
    print(c.dimensions)      # (9, 13)
    print(c.grille[0])       # "#############"
    print(c.depart_robot)    # (6, 1)
    print(c.armoire_pos)     # (6, 4)
    print(c.dico_pos)        # (7, 6)
    print(c.residents)       # {'R1': ('Camille', (6, 11)), 'R2': ('Hugo', (3, 3))}

if __name__ == "__main__":
    main()