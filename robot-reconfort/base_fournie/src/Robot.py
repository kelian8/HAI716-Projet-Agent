from __future__ import annotations
from Carte import Carte
from collections import deque
from Exceptions import ErreurEtat
from etats import creer_etats
from etats.etat import Etat

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Simulation import Simulation 

class Robot:

    DIRECTIONS = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "O": (0, -1)
    }

    parent : Simulation

    position : tuple[int,int]
    carte : Carte #TODO enlever ça (donc enlever les appels à carte dans la fonction naviguer_vers pour bien s'assurer que le robot n'a pas accès à la carte)
    #dictionnaire de dictionnaire key1 = emotion key1.x = intensité et valeur =position du casier dans l'armoire et objet(eventuellement null)
    #ne sert pas a grand chose pour l'instant si ce n'est savoir si un casier est eventuellement vide et si c'est le cas et qu'on a besoin de l'objet 
    #correspondant, nous irons a un casier ayant une emotion/intensite proche de celle recherchée initialement
    armoire_connue : dict
    objet_tenu : str | None 
    current_demande : dict |None #demande qu'on traite actuellement
    listeEtats: dict[str,Etat]
    etat : Etat | None #etat actuel du robot (recherche x, cherche dans armoire, etc )
    emotion_intensite : tuple[str,str] | None
    objectif : str #Objetif du robot : "armoire", "dictionnaire" ou "resident"

    def __init__(self,parent:Simulation):
        self.parent = parent

        self.position = parent.get_robot_depart()
        self.position_armoire = parent.get_casier_depart() #ca c'est la position du sélecteur dans l'armoire mdr
        self.grille_connue = self.generer_grille_perso()
        #la carte donnée au robot lors de son initialisation dans "simulation", est une carte creer par simulation dont la grille a été remplacxe par une gerille
        #"vierge" a l'execption des residents, l'armoire, et le dico 
        self.dico_pos = self.parent.scenario.carte.get_position("dictionnaire")
        self.armoire_pos = self.parent.scenario.carte.get_position("armoire")
        self.armoire_connue= {}
        self.objet_tenu=None
        self.current_demande = None
        self.listeEtats = creer_etats(self)
        self.etat = None
        self.changer_etat("EtatInit")
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

        dimensionCarte = self.parent.get_carte_size() #dimensionCarte[0] = hauteur, dimensionCarte[1] = largeur


        grille = [["." for _ in range(dimensionCarte[1])]for _ in range(dimensionCarte[0])]

        #le robot connaît sa position de départ.
        ligne, colonne = self.position
        grille[ligne][colonne] = "."

        #il connaît les positions des elements.
        ligne, colonne = self.parent.get_armoire_pos()
        grille[ligne][colonne] = "A"

        ligne, colonne = self.parent.get_dico_pos()
        grille[ligne][colonne] = "D"

        for resident in self.parent.get_residents():
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
        if self.etat != None:
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

        dimensionCarte = self.parent.get_carte_size()
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
                0 <= l < dimensionCarte[0]
                and 0 <= c < dimensionCarte[1]
            ):
                continue

            symbole_reel = self.parent.get_symbole(l,c)
            perceptions[direction] = symboles[symbole_reel]

        return perceptions


    
    def mettre_a_jour_grille_connue(self, perceptions):
        """
            args: 
                rien

            return:
                dico du contenu des cases voisines a celles du robot
        
            what it does
                met a jour la grille perso du robot avec les elements des cases voisines.
        """

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

        # verif des limites
        if not (0 <= nouvelle_ligne < self.parent.get_carte_size()[0]
            and 0 <= nouvelle_colonne < self.parent.get_carte_size()[1]):

            print("Déplacement impossible : hors de la grille")
            return False

        symbole = self.parent.get_symbole(nouvelle_ligne,nouvelle_colonne)

        #on verifie que les cases sont des cases traversables
        if symbole not in (".", "R"):
            print(f"Obstacle inattendu en "f"({nouvelle_ligne}, {nouvelle_colonne})")
            self.grille_connue[nouvelle_ligne][nouvelle_colonne] = "#"
            return False

        self.position = (nouvelle_ligne, nouvelle_colonne)#deplacement du robot

        print(f"Déplacement {direction} : position {self.position}")

        return True

    def calculer_chemin(self, destinations)->list[tuple[int,int]]:
        """
        args: 
            destination a laquelle le robot doit se rendre 

        return : 
            rien 

        what it does :  
            calcule un chemin entre la position du robot et la destination en se basant sur la grille perso du robot.
           on suppose les cases inconnues sont libres
        """

        depart = self.position
        destinations = {tuple(p) for p in destinations}

        if depart in destinations:
            return [depart]

        hauteur = len(self.grille_connue)
        largeur = len(self.grille_connue[0])

        file = deque([depart])
        predecesseurs:dict[tuple[int,int],tuple[int,int] | None] = {depart: None}

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

        return []


############################fonctions pour la recherche d'objet dans l'armoire######################################


    def chercher(self, direction):
        """
        args:
            la direction dans laquelle on deplace le selcteur 
        
        return: 
            bool indiquant si le deplacement est possible

        what it does:
            deplace le selecteur dans l'armoire si cela est possible 
            et met a jour la memoire du robot
        """

        if direction not in self.DIRECTIONS:
            raise ValueError("Direction inconnue")

        #position du selecteur avant l'action
        ancienne_position = self.position_armoire
        ligne, colonne = ancienne_position

        dl, dc = self.DIRECTIONS[direction]

        nouvelle_ligne = ligne + dl
        nouvelle_colonne = colonne + dc

        #les lignes ne bouclent pas comme les emotions donc on verifie
        if not (0 <= nouvelle_ligne < 3):
            print("Déplacement impossible : hors de l'armoire")
            return False

        # les colonnes, quant a elles, bouclent donc on fait un modulo 8 (car 8 emotions)
        nouvelle_colonne = nouvelle_colonne % 8

        nouvelle_position = (nouvelle_ligne, nouvelle_colonne)

        #on regarde dans le casier atteint
        objet = self.parent.get_armoire().get_objet(nouvelle_ligne, nouvelle_colonne)

        #on enregistre l'action dans la trace
        # puis on transmet bien l'ancienne position du sélecteur avant le deplacement
        if self.current_demande != None:
            self.parent.trace.ajouter_pas(
                self.current_demande["numero"],
                self.position,
                ancienne_position,
                "CHERCHER",
                argument=direction,
                contenu_casier=objet
            )

        #on met a jour la position et la mémoire du robot
        self.position_armoire = nouvelle_position
        self.armoire_connue[nouvelle_position] = objet

        return True


    def prendre(self):
        """
        args:
            rien
        return : 
            bool indiquant si l'objet a pu etre attrapé par le robot

        what it does:
            prends l'objet du casier courant s'il nest pas vide, met a jour l'armoire et la memoire du robot 
        """

        position = self.position_armoire
        ligne, colonne = position

        #on verifie que le robot ne tient pas deja un objet
        if self.objet_tenu is not None:
            print("Le robot tient déjà un objet.")
            return False

        #on verifie que le contenu du casier est connu
        if position not in self.armoire_connue:
            print("Le contenu de ce casier n'est pas connu.")
            return False

        objet = self.armoire_connue[position]

        # on verifie que le casier n'est pas vide
        if objet is None:
            print("Ce casier est vide.")
            return False

        # on fait la trace de l'action avant de modifier le contenu de l'armoire
        if self.current_demande is not None:
            self.parent.trace.ajouter_pas(
                self.current_demande["numero"],
                self.position,
                position,
                "PRENDRE",
                argument=objet,
                contenu_casier=objet
            )

        #le robot prend l'objet
        self.objet_tenu = objet

        #le casier devient vide dans l'armoire réelle
        self.parent.get_armoire().add_objet(ligne, colonne, None)

        # et on met a jour la memoire de l'armoire du robot
        self.armoire_connue[position] = None

        print(f"Le robot a pris : {objet}")

        return True


    def observer_casier(self):
        """
        args :
            rien
        return :
            objet contenu dans un casier
        what it does :
            observe le contenu d'un casier, mais sert surtout a regler le probleme si le casier cible est le casier 
            sur lequel le selecteur est initialement postionné        
        """
        ligne, colonne = self.position_armoire
        objet = self.parent.get_armoire().get_objet(ligne, colonne)

        self.armoire_connue[self.position_armoire] = objet

    #on oublie pas de faire la trace quand meme
        if self.current_demande is not None:
            self.parent.trace.ajouter_pas(
                self.current_demande["numero"],
                self.position,
                self.position_armoire,
                "OBSERVER",
                contenu_casier=objet
            )

        return objet

########################################################################
#toutes ces fonctions iront dans chaque classe de "état" correspondantes, 
#(ex: chercherDansArmoire, majArmoire, prendreObjet seront des fonctions de l'etat "recherche_dans_l'armoire" )
########################################################################


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
