le robot fait appel a simulation_step qui fait appel a :
self.etat.simulation_step()

self.etat.simulation_step() est une fonction commune a tous les etats,
son comportement est different selon l'etat dans lequel se trouve le robot

EtatAttente :
pas grand chose a expliqué cest assez clair 



EtatNavigation :
verifie que le robot n'est pas deja sur une case adjacente a la position
sinon
fait appel a naviguer_vers (fonction contenue dans la classe robot) avec la postion du dico obtenue grace a get_position("dictionnaire") (contenue dans la classe carte)
puis une fois arriver a la destination on change d'etat vers consulter 

