from Carte import *
from EtatAttente import *
from collections import deque
from Simulation import Simulation
from Etat import creer_etats

class ErreurEtat()

class Robot:

    DIRECTIONS = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "O": (0, -1)
    }

    parent : Simulation

    position : tuple
    carte : Carte #TODO enlever ça (donc enlever les appels à carte dans la fonction naviguer_vers pour bien s'assurer que le robot n'a pas accès à la carte)
    grille 
    dico_pos
    #dictionnaire de dictionnaire key1 = emotion key1.x = intensité et valeur =position du casier dans l'armoire et objet(eventuellement null)
    #ne sert pas a grand chose pour l'instant si ce n'est savoir si un casier est eventuellement vide et si c'est le cas et qu'on a besoin de l'objet 
    #correspondant, nous irons a un casier ayant une emotion/intensite proche de celle recherchée initialement
    armoire_connue : dict
    objet_tenu : str | None 
    current_demande : dict |None #demande qu'on traite actuellement
    listeEtats: list[Etat]
    etat : Etat #etat actuel du robot (recherche x, cherche dans armoire, etc )
    emotion_intensite : [str,str] | None

    def __init__(self,parent):
        self.parent = parent

        self.position = parent.get_robot_depart
        self.grille_connue = self.generer_grille_perso()
        #la carte donnée au robot lors de son initialisation dans "simulation", est une carte creer par simulation dont la grille a été remplacxe par une gerille
        #"vierge" a l'execption des residents, l'armoire, et le dico 
        self.dico_pos = self.simulation.scenario.carte.get_position("dictionnaire")
        self.armoire_connue= {}
        self.objet_tenu=None
        self.current_demande = None
        self.listeEtats = creer_etats(robot)
        self.etat = None
        changer_etat("EtatInit")
        self.emotion_intensite = None


    def generer_grille_perso(self):
        """
        args:
            rien

        return :
            tableau de tableau de char

        what it does : 
            creer la grille la grille perso (vierge) du robot sans lire les murs.
        """

        dimensionCarte = simulation.get_carte_size() #dimensionCarte[0] = hauteur, dimensionCarte[1] = largeur


        grille = [[None for _ in range(dimensionCarte[1])]for _ in range(dimensionCarte[0])]

        #le robot connaît sa position de départ.
        ligne, colonne = self.position
        grille[ligne][colonne] = "."

        #il connaît les positions des elements.
        ligne, colonne = self.simulation.get_armoire_pos()
        grille[ligne][colonne] = "A"

        ligne, colonne = self.simulation.get_dico_pos()
        grille[ligne][colonne] = "D"

        for resident in self.simulation.get_residents
            ligne, colonne = resident["position"]
            grille[ligne][colonne] = "P"

        return grille

        
    """
        inutile mais on garde au cas ou 
        [["." for j in range(taillecarte[0])] for i in range(taillecarte[1])]
    
        #boucle pour rentrer les bordures
        for j in carte.grille:

            #pour la bordure haute et basse
            if j==0 or j==taillecarte[0]:
                for i in range(0,taillecarte[1]):
                    carte[j][i]="#"

            #pour la bordure droite et gauche        
            elif i==0 or i==taillecarte[1]:
                carte[j][i]="#"

        #pour la position des residents
        for k in carte.residents : 
            pass
"""

############################fonctions pour le deplacement/mise ajour grille du robot######################################

    def percevoir_voisins(self):
        """
        args : 
            rien
        
        return :
            dico du contenu des cases voisines

        what it does : 
            regarde les quatre cases adjacentes au robot dans la grille
            réelle et renvoit le resultat.
        """

        grille_reelle = self.carte.grille
        dimensionCarte = self.simulation.get_carte_size()
        ligne, colonne = self.position

        symboles = {
            "#": "mur",
            ".": "libre",
            "R": "libre",
            "A": "armoire",
            "D": "dictionnaire",
            "P": "resident"
        }

        perceptions = {}

        for direction, (dl, dc) in self.DIRECTIONS.items():
            l = ligne + dl
            c = colonne + dc

            # Hors de la grille : aucune case à observer.
            if not (
                0 <= l < len(dimensionCarte[0])
                and 0 <= c < len(dimensionCarte[1])
            ):
                continue

            symbole_reel = self.simulation.get_symbole(l,c)
            perceptions[direction] = symboles[symbole_reel]

        return perceptions


    
    def mettre_a_jour_grille_connue(self):
        """
            args: 
                rien

            return:
                dico du contenu des cases voisines a celles du robot
        
            what it does
                met a jour la grille perso du robot avec les elements des cases voisines.
        """

        perceptions = self.percevoir_voisins() #on recup les element des cases voisines

        symboles = {
            "mur": "#",
            "libre": ".",
            "armoire": "A",
            "dictionnaire": "D",
            "resident": "P"
        }

        ligne, colonne = self.position

        for direction, contenu in perceptions.items():
            dl, dc = self.DIRECTIONS[direction] #on recupere les "modificateurs" de positions des direction

            #calcul des cases voisines selon les "modificateurs"
            l = ligne + dl
            c = colonne + dc

            self.grille_connue[l][c] = symboles[contenu] #met a jour la grille

            if contenu == "mur":
                print(f"Mur découvert en ({l}, {c})")

        return perceptions


    def avancer(self, direction):
        """
            args: 
                direction de deplacement du robot O,S,N,E

            return :
                bool indiquant si le deplacement a pu etre effectue

            what it does : 
                effectue  le deplacement du robot dans la grille si il est possible et renvoit true, sinon pas
                de deplacement et renvoit false.
                
        """

        if direction not in self.DIRECTIONS:
            raise ValueError("Direction inconnue")

        dl, dc = self.DIRECTIONS[direction]

        nouvelle_ligne = self.position[0] + dl
        nouvelle_colonne = self.position[1] + dc

        grille_reelle = self.carte.grille

        # verif des limites
        if not (0 <= nouvelle_ligne < len(grille_reelle)
            and 0 <= nouvelle_colonne < len(grille_reelle[0])):

            print("Déplacement impossible : hors de la grille")
            return False

        symbole = grille_reelle[nouvelle_ligne][nouvelle_colonne]

        #on verifie que les cases sont des cases traversables
        if symbole not in (".", "R"):
            print(f"Obstacle inattendu en "f"({nouvelle_ligne}, {nouvelle_colonne})")
            self.grille_connue[nouvelle_ligne][nouvelle_colonne] = "#"
            return False

        self.position = [nouvelle_ligne, nouvelle_colonne]#deplacement du robot

        print(f"Déplacement {direction} : position {self.position}")

        return True




    def calculer_chemin(self, destinations):
        """
        args: 
            destination a laquelle le robot doit se rendre 

        return : 
            rien 

        what it does :  
            calcule un chemin entre la position du robot et la destination en se basant sur la grille perso du robot.
           on suppose les cases inconnues sont libres
        """

        depart = tuple(self.position)
        destinations = {tuple(p) for p in destinations}

        if depart in destinations:
            return [depart]

        hauteur = len(self.grille_connue)
        largeur = len(self.grille_connue[0])

        file = deque([depart])
        predecesseurs = {depart: None}

        while file:
            courant = file.popleft()

            if courant in destinations:
                chemin = []
                case = courant

                while case is not None:
                    chemin.append(case)
                    case = predecesseurs[case]

                chemin.reverse()
                return chemin

            for dl, dc in self.DIRECTIONS.values():
                l = courant[0] + dl
                c = courant[1] + dc
                voisin = (l, c)

                if not (0 <= l < hauteur and 0 <= c < largeur):
                    continue

                if voisin in predecesseurs:
                    continue

                contenu = self.grille_connue[l][c]

                # Une case inconnue est supposée libre.
                # Les murs et les éléments ne sont pas traversables.
                if contenu not in (None, "."):
                    continue

                predecesseurs[voisin] = courant
                file.append(voisin)

        return None

    #les fonctions (calculer_chemin,avancer,mettre_a_jour_grille_connue,percevoir_voisins) sont utilisées dans cette fonction
    def naviguer_vers(self, position_cible):
        """
            args:
                destination 

            return :
                bool true si le robot est arrive a la destination et false sinon

            what it does:
                fait naaviguer le robot jusqu'à une case adjacente a destination.

                a chaque deplacement :
                    on percoit les cases voisines
                    on met à jour la grille perso du robot
                    on recalcule le chemin
                    et on avance d'une case
        """

        cible = tuple(position_cible)

        while True:

            #decouverte des cases autour du robot
            self.mettre_a_jour_grille_connue()

            #les cases adjacentes a la cible sont les destinations
            #on calcul la positions des cases adjacentes a la destinantion
            destinations = []

            for dl, dc in self.DIRECTIONS.values():
                l = cible[0] + dl
                c = cible[1] + dc

                if not (
                    0 <= l < len(self.grille_connue)
                    and 0 <= c < len(self.grille_connue[0])
                ):
                    continue

                contenu = self.grille_connue[l][c]

                if contenu in (None, "."):
                    destinations.append((l, c))

            #on verifie si le robot est arrive a une des destinations
            if tuple(self.position) in destinations:
                print(f"Destination atteinte depuis {self.position}")
                return True

            #calcul de l'itineraire a partir de la grille perso du robot.
            chemin = self.calculer_chemin(destinations)

            if chemin is None:
                print("Aucun chemin connu vers la cible.")
                return False

            print("Chemin calculé :", chemin)

            #on se deplace, puis on recommence la boucle pour verifier tout ce qu'on vient de verifier
            prochaine_case = chemin[1]

            dl = prochaine_case[0] - self.position[0]
            dc = prochaine_case[1] - self.position[1]

            #pour renvoyer la direction correspondant a (dl,dc)
            direction = None
            for nom, delta in self.DIRECTIONS.items():
                if delta == (dl, dc):
                    direction = nom
                    break
            

            #si deplacement pas possible on recalcul un itinineraire
            if not self.avancer(direction):
                print("Recalcul du chemin apres l'obstacle...")
                continue



############################fonctions pour le deplacement/mise ajour grille du robot######################################



    def changer_etat(self, nouvel_etat:str):
            """args : 
                le nouvel etat

            return :
                rien

            
            what it does : 
                Effectue une transition entre deux états.
                sort de l'etat courant 
                entre dans le nouvel etat
            """

            if self.etat is not None:
                self.etat.exit()

            try:
                prochain_etat = self.listeEtats[nouvel_etat]
            except KeyError as e:
                raise ErreurEtat(f"L'état {nouvel_etat} n'existe pas")

            self.etat = prochain_etat
            self.etat.enter()




    def simulation_step(self):
            """
        args : 
            rien
        
        return : 
            rien
        
        what it does : 
            fait avancer la simulation du robot, fera appel a etat.simulation_step() qui via les differents etats :
            gerera l'itiniraire du robot à adopté, s'occupera du deplacement, de la
            verification de la position du robot par rapport a son "objectif" actuel,
            appels aux fonctions en conséquences, mettra a jour la carte etc
        """

        self.etat.simulation_step()




    def est_adjacent(self, position_cible):
        """
        args : 
            position recherchée
        
        return :
            bool

        what it does : 
            indique si le robot est sur une case adjacente de la position recherchee.
        
    """

        if position_cible is None:
            return False

        ligne_robot, colonne_robot = self.position
        ligne_cible, colonne_cible = position_cible

        distance = (
            abs(ligne_robot - ligne_cible)
            +abs(colonne_robot - colonne_cible))

        return distance == 1






















########################################################################
#toutes ces fonctions iront dans chaque classe de "état" correspondantes, 
#(ex: chercherDansArmoire, majArmoire, prendreObjet seront des fonctions de l'etat "recherche_dans_l'armoire" )
########################################################################





def majArmoire(key1,key2):
    """
    args : 
        Key1 : str contenant l'emotion
        Key2 : str contenant l'intensite de l'emotion

    return: 
        rien


    what it does : 
        met a jour l'armoire connue du robot, en mettant a jour le dico de dico avec key1 : key2 : [position casier dans l'armoire, objet contenu dans casier]
    """
    pass

def chercherDansArmoire(emotion, intensite):
    """
    args : 
        emotion : str contenant l'emotion recherchée
        intensite : str contenant l'intensité recherchée

    return : 
        1 si objet correspondant trouvé 0 sinon

    what it does : 
        est appele  quand le robot est sur une case adjacente a l'armoire et que le robot est dans un etat "chercher armoire"
        parcours de casier en casier jusqu'a l'emotion/intensité recherchées en mettant a jour l'armoire_connue du robot.
        fait appel a prendreObjet si l'objet correspond a l'emotion/intensite et remplace l'objet du casier a None dans l'armoire et l'armoire_connue du robot
        TODO faire une enum globale pour passer d'une emotion/intensité a un couple (ligne, colonne) pour se reprer dans l'armoire
    """
    pass

def prendreObjet(obj):
    """
    args : 
        obj : str le nom de l'objet qu'on prend

    return : 
        rien

    what it does : 
        prend l'objet = met a jour robot.objet_tenu avec l'objet prit 
    
    """
    pass

def donnerObjet(resident):
    """
    args : 
        resident : str resident recevant l'objet

    return : 
        rien

    what it does : 
        est appele quand le robot est sur une case adjacente au resident correspondant a la demande que nous sommes en train de traiter 
        ET 
        que le robot tient un objet
        ET 
        est dans l'etat "acheminement de l'objet au resident"
        donne l'objet au resident et met a jour robot.objet_tenu
    """
    pass
