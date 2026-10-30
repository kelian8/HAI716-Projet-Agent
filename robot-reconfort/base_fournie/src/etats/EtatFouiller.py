from .etat import Etat
from Constantes import EMOTIONS_ORDRE, INTENSITES_ORDRE


class EtatFouiller(Etat):



    def enter(self):
        print("Le robot commence à fouiller dans l'armoire.")
        self.candidats = self.construire_candidats()#construction des casier candidats dans l'ordre de prioriete 
        self.indice_candidat = 0#indice du candidat le plus prioritaire actuel
        self.chemin = []

    def exit(self):
        print("Le robot quitte l'état de fouille.")



    def simulation_step(self):
        #cas ou tous les candidats ont été parcouru 
        if self.indice_candidat >= len(self.candidats):
            print("Aucun objet disponible dans les casiers candidats.")
            # TODO : gérer l'absence d'objet
            return

        cible = self.candidats[self.indice_candidat]

        #si on sait deja que le casier cible est vide on change de casier cible
        if cible in self.robot.armoire_connue:
            if self.robot.armoire_connue[cible] is None:
                self.indice_candidat += 1
                return

        #si le selecteur n'est pas devant le candidat, on se deplace 
        if self.robot.position_armoire != cible:
            self.aller_vers_casier(cible)
            return


        #le selecteur est arrive devant le casier cible 
        #on doit connaitre son contenu pour décider quoi faire.

        #ce cas est possible si le selecteur est deja initialement positionne sur le casier cible
        if cible not in self.robot.armoire_connue:
            """print("PAS NORMAL : Le contenu de ce casier n'a pas encore été observé.")
            return
            """
            self.robot.observer_casier()#on regle lce cas la grace a ca, car sinon le casier n'a jamais ete observe car
                                        #on s'est jamais deplace dessus

        #si on est tombé sur un casier ne contenant rien on passe au casier candidat suivant 
        objet = self.robot.armoire_connue[cible]

        if objet is None:
            self.indice_candidat += 1
            return

        #quand le bon a été trouvé, on le prend et on passe a l'etat suivant
        if self.robot.prendre():
            print("Objet récupéré, fin de la fouille.")
            self.robot.changer_etat("EtatNavigationResident")



    def __str__(self):
            return "Etat Fouiller"



    def construire_candidats(self):
        """
        args : 
            rien

        return :
            liste d'emotions candidates

        what it does : 
            determine une liste d'emotions candidate pour la recherche dans le casier classées par ordre de correspondance
        """
        emotion_demandee, intensite_demandee = self.robot.emotion_intensite

        colonne_demandee = EMOTIONS_ORDRE.index(emotion_demandee)
        ligne_demandee = INTENSITES_ORDRE.index(intensite_demandee)

        candidats = []

        for ligne in range(3):
            for colonne in range(8):

                #distance des emotions entre l'emotion courante et l'emotion demandée sur la roue des emotions
                distance_horaire = (colonne - colonne_demandee) % 8
                distance_antihoraire = (colonne_demandee - colonne) % 8

                distance_emotion = min(
                    distance_horaire,
                    distance_antihoraire
                )

                #on ignore les émotions situées à plus de 2 positions
                if distance_emotion > 2:
                    continue

                distance_intensite = abs(ligne - ligne_demandee)

                #on garde le sens horaire prioritaire en cas d'egalité de distance entre 2 emotions
                sens = 0 if distance_horaire <= distance_antihoraire else 1

                candidats.append((
                    distance_emotion,
                    distance_intensite,
                    ligne,
                    sens,
                    (ligne, colonne)))

        candidats.sort()

        return [candidat[4] for candidat in candidats]

    

    def aller_vers_casier(self, cible):
        """
        args:
            cible est un tuple de int permettant de designer le le casier cible

        return:
            bool signifiant si le deplacement a ete possible ou si le selecteur est sur le bon casier

        what it does :
            deplace le selecteur de casier un part un, dabord verticallement puis horizontallement ensuite
        """

        ligne_actuelle, colonne_actuelle = self.robot.position_armoire
        ligne_cible, colonne_cible = cible

        # on se deplace verticalement d'abord
        if ligne_actuelle < ligne_cible:
            return self.robot.chercher("S")

        elif ligne_actuelle > ligne_cible:
            return self.robot.chercher("N")

        #Puis horizontalemment ensuite
        if colonne_actuelle != colonne_cible:

            #on regarde quelle est le chemin est le plus court pour atteindre la bonne colonne (si on part vers la droite ou la gauche)
            distance_est = (colonne_cible - colonne_actuelle) % 8
            distance_ouest = (colonne_actuelle - colonne_cible) % 8

            if distance_est <= distance_ouest:
                return self.robot.chercher("E")
            else:
                return self.robot.chercher("O")

        #quand le selecteur est sur le bon casier
        return True

