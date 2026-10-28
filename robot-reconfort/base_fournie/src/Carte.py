class Carte:

    def __init__(self, dimensions:tuple[int,int], grille, depart_robot, armoire_pos, dico_pos, residents):
        self.dimensions = dimensions
        self.grille = grille
        self.depart_robot = depart_robot
        self.armoire_pos = armoire_pos
        self.dico_pos = dico_pos
        self.residents = residents



    #TODO est ce qu'on peut pas passer cette fonction dans simulation ? comme ça elle evite les self.simulation.scenario.carte.get_position
    def get_position(self, element, resident_id=None)->tuple[int,int]:
        """
        args : 
            l'element recherche et son id s'il s'agit d'un resident

        return :
             la position de cette element sur la grille

        
        what it does : 
            Retourne la position d'une armoire, du dictionnaire ou d'un résident.
        """

        if element == "armoire":
            return self.armoire_pos

        elif element == "dictionnaire":
            return self.dico_pos

        elif element == "resident":
            for resident in self.residents:
                if resident["id"] == resident_id:
                    return resident["position"]

        return (-1,-1) #TODO faire des vérifs que la position reçue par cette fonction est correcte
