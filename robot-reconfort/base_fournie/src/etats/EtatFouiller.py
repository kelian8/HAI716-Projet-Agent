from Etat import Etat
from Robot import *

class EtatFouiller(Etat):

    def enter(self):
        print("Le robot fouille dans l'armoire.")


    def exit(self):
        
        print("Le robot a fini de fouiller dans l'armoire.")

    def simulation_step(self):
        pass#TODO

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