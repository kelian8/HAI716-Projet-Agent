from .etat import Etat

class EtatFouiller(Etat):


    EMOTIONS = [
    "joie",
    "confiance",
    "peur",
    "surprise",
    "tristesse",
    "degout",
    "colere",
    "anticipation"
    ]

    INTENSITES = ["faible", "moyenne", "forte"]


    def enter(self):
        print("Le robot fouille dans l'armoire.")


    def exit(self):
        
        print("Le robot a fini de fouiller dans l'armoire.")

    def simulation_step(self):
        pass#TODO




    def majArmoire(self, casier):
        """
        args : 
            Key1 : str contenant l'emotion
            Key2 : str contenant l'intensite de l'emotion

        return: 
            rien


        what it does : 
            met a jour l'armoire connue du robot, en mettant a jour le dico de dico avec key1 : key2 : [position casier dans l'armoire, objet contenu dans casier]
        """
        emotion = casier["emotion"]
        intensite = casier["intensite"]

        if emotion not in self.robot.armoire_connue:
            self.robot.armoire_connue[emotion] = {}

        self.robot.armoire_connue[emotion][intensite] = {
            "position": [casier["ligne"], casier["colonne"]],
            "objet": casier["objet"]}

        print(f"Casier observé et mis a jour : {emotion}, {intensite} "f"-> {casier['objet']}")



        def distance_emotion(self, emotion_demandee, emotion_casier):
            """
            args:
                emotion_demandé : str representant l'emotion que l'on recherche
                emotion_casier : str representant l'emotion contenue dans le casier 

            return : 
                int representant la distance entre les 2 emotions
            
            what it does :
                calcule la distance circulaire entre deux émotions
                on considere que les colonnes 0 et 7 sont voisines
            """

            col_demandee = self.EMOTIONS.index(emotion_demandee)
            col_casier = self.EMOTIONS.index(emotion_casier)

            distance = abs(col_demandee - col_casier)

            return min(distance, 8 - distance)#pour compter soit dans le sens horaire ou 
                                              #le sens anti_horaire si moins eloigne dans la roue de Plutchik



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

    def __str__(self):
        return "Etat Fouiller"