le robot fait appel a simulation_step qui fait appel a :
self.etat.simulation_step()

self.etat.simulation_step() est une fonction commune a tous les etats,
son comportement est different selon l'etat dans lequel se trouve le robot

EtatInit :
Initialisations avant d'entrer dans la boucle de logique

EtatAttente :
Le robot fetch une demande, une fois une demande assignée, transition vers EtatNavigationDico

EtatNavigationDico :
verifie que le robot n'est pas deja sur une case adjacente a la position
sinon
fait appel a naviguer_vers (fonction contenue dans la classe robot) avec la postion du dico obtenue grace a get_position("dictionnaire") (contenue dans la classe carte)

EtatNavigationArm : idem mais pous aller vers l'armoire

EtatFouiller : une fois adjacent à l'armoire, le robot fouille dedans pour soit 1- trouver un objet, soit 2- ne pas trouver d'objet (passer à la demande suivante)

EtatNavigationRes : navigation vers résident, une fois atteint, donne l'objet et revient en attente



