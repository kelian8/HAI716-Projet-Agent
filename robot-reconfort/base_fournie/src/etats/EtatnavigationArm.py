from .etat import Etat

class EtatNavigationArm(Etat):

    destinations:list[tuple[int,int]] = []
    chemin:list[tuple[int, int]]

    def enter(self):
        print("Le robot commence à se déplacer vers le l'armoire.")
        #les cases adjacentes a la cible sont les destinations
        #on calcul la positions des cases adjacentes a la destinantion
    
        for dl, dc in self.robot.DIRECTIONS.values():
            l = self.robot.armoire_pos[0] + dl
            c = self.robot.armoire_pos[1] + dc

            if not (
                0 <= l < len(self.robot.grille_connue)
                and 0 <= c < len(self.robot.grille_connue[0])
            ):
                continue

            contenu = self.robot.grille_connue[l][c]

            if contenu in (None, "."):
                self.destinations.append((l, c))

        #calcul de l'itineraire a partir de la grille perso du robot.
        self.chemin = self.robot.calculer_chemin(self.destinations)


    def exit(self):
        
        print("Le robot quitte l'état de navigation vers l'armoire.")

    def simulation_step(self):
        print("le robot se deplace vers l'armoire")
        if not self.robot.est_adjacent(self.robot.armoire_pos): #verifie si le robot est sur une case adjacente
                                                                                        #à l'armoire
            if len(self.chemin) == 0 :
                print("Aucun chemin connu vers l'armoire.")
                raise ValueError("Armoire inateignable")
            print("Chemin calculé :", self.chemin)

            perceptions = self.robot.percevoir_voisins() #on recup les element des cases voisines
            self.robot.mettre_a_jour_grille_connue(perceptions) #decouverte des cases autour du robot

            prochaine_case = self.chemin[1]
            self.chemin.pop(0)

            dl = prochaine_case[0] - self.robot.position[0]
            dc = prochaine_case[1] - self.robot.position[1]

            #pour renvoyer la direction correspondant a (dl,dc)
            direction = None
            for nom, delta in self.robot.DIRECTIONS.items():
                if delta == (dl, dc):
                    direction = nom
                    break

            #Ajouter dans la trace ici : on a toutes les infos avant le déplacement
            if self.robot.current_demande != None:
                self.robot.parent.trace.ajouter_pas(
                    self.robot.current_demande["numero"],
                    self.robot.position,
                    self.robot.position_armoire,
                    "AVANCER",
                    direction,
                    perceptions,
                )

            #Si le robot a découvert un obstacle sur le chemin et n'a pas pu avancer,
            #  recalcul du chemin pour se déplacer au pas suivant
            if not self.robot.avancer(direction):
                print("Recalcul du chemin apres l'obstacle...")
                self.chemin = self.robot.calculer_chemin(self.destinations)
                

        else:
            print("le robot est bien arrivé à l'armoire.")
            self.robot.changer_etat("EtatFouiller")