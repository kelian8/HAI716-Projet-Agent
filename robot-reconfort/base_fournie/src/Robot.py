from Carte import *


class Robot:

    position : tuple
    carte : Carte
    #dictionnaire de dictionnaire key1 = emotion key1.x = intensité et valeur =position du casier dans l'armoire et objet(eventuellement null)
    #ne sert pas a grand chose pour l'instant si ce n'est savoir si un casier est eventuellement vide et si c'est le cas et qu'on a besoin de l'objet 
    #correspondant, nous irons a un casier ayant une emotion/intensite proche de celle recherchée initialement
    armoire_connue : dict
    objet_tenu : str | None 
    current_demande : dict |None #demande qu'on traite actuellement
    etat : xxx #etat actuel du robot (recherche x, cherche dans armoire, etc )
    emotion_intensite : [str,str] | None

    def __init__(self,carte):
        self.position = carte.depart_robot
        
        #la carte donnée au robot lors de son initialisation dans "simulation", est une carte creer par simulation dont la grille a été remplacxe par une gerille
        #"vierge" a l'execption des residents, l'armoire, et le dico 
        self.carte = carte
        self.armoire_connue= {}
        self.objet_tenu=None
        self.current_demande = None
        self.etat = xxx #a remplacer
        self.emotion_intensite = None


        
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


def simulation():
    """
    args : 
        rien
    
    return : 
        rien
    
    what it does : 
        fait avancer la simulation du robot, fera appel a etat.process() qui via les differents etats :
        gerera l'itiniraire du robot à adopté, s'occupera du deplacement, de la
        verification de la position du robot par rapport a son "objectif" actuel,
         appels aux fonctions en conséquences, mettra a jour la carte etc
    """
    
    pass

########################################################################
#toutes ces fonctions iront dans chaque classe de "état" correspondantes, 
#(ex: chercherDansArmoire, majArmoire, prendreObjet seront des fonctions de l'etat "recherche_dans_l'armoire" )
########################################################################


def deplacement(direction):
    """
    args : 
        direction : str S|N|O|E pour savoir dans quelle direction on se deplace si c'est possible

    return : 
        retourne 1 si deplacement possible et -1 sinon

    what it does : 
        s'occupe du deplacement du robot sur la grille, verifie si le deplacement demandé est realisable, met a jour la position courante du robot
    """
    pass

def majCarte():
    """
    args : 
        rien
    
    return :
        rien

    what it does : 
        met a jour la Carte.grille connue du robot, met les cases au Nord,Sud,Ouest,Est du robot a jour 
    
    """
    pass

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

def consulter(): 
    """ 
    args : 
        rien
    
    return : 
        rien

    what it does : 
        cherche l'emotion/intensité correspondantes a la phrase de la demande qu'il dont il s'occupe actuellemment
        et met a jour l'attribut "emotion_intensite" du robot par l'emotion et l'intensité correspondante a la phrase
    """
