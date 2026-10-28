from Etat import Etat
from Robot import *
from Carte import *
from reconfort_io import normaliser

class EtatNavigationDico(Etat):

    def enter(self):
        print("Le robot commence à se déplacer vers le dico.")


    def exit(self):
        
        print("Le robot quitte l'état de navigation vers le dico.")

    def simulation_step(self):
        arrive=False
        print("le robot se deplace vers le dictionnaire")
        if not self.robot.est_adjacent(self.robot.dico_pos): #verifie si le robot est sur une case adjacente
                                                                                        #au dico
            arrive = self.robot.naviguer_vers(self.robot.dico_pos)#fait la naviguation vers le dico 
        else:
            arrive=True


        if arrive:
            print("le robot est bien arrivé au dictionnaire.")
            self.robot.emotion_intensite = self.consulter()
            if self.robot.emotion_intensite == None :
                print("Aucune émotion n'a pu être associée à la demande. Le robot passe à la demande suivante")
                self.robot.changer_etat("EtatAttente")
            else :
                print("Le robot a trouvé une correspondance dans le dictionnaire")
                self.robot.changer_etat("EtatNavigationArm")


    def consulter(self): 
        """ 
        args : 
            rien
        
        return : 
            rien

        what it does : 
            cherche l'emotion/intensité correspondantes a la phrase de la demande qu'il dont il s'occupe actuellemment
            et met a jour l'attribut "emotion_intensite" du robot par l'emotion et l'intensité correspondante a la phrase
        """
        if self.robot.current_demande == None:
            return None
        mots = normaliser(self.robot.current_demande["message"])
        for mot in mots:
            if mot in self.robot.parent.dictionnaire:
                return self.robot.parent.dictionnaire["message"]
        return None
