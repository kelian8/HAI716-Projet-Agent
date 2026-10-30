# Robot de réconfort — BAEZA & HOURMAND

Projet de semestre, master informatique. Un robot à perception locale
consulte un dictionnaire, fouille une armoire et rapporte un objet à un
résident.

Langage : **Python** — Version : **3.10+**

## Lancer

Pour lancer le projet se placer dans le dossier **base_fournie** puis exécuter la comande suivante :
```
**python Projet.py** <scenario.json> <dossier_donnees> <trace_sortie.json>
```
La carte **n'est plus** à renseigner puisqu'elle est trouvable directement dans le fichier de scénario

Exemple :

```
python Projet.py cartes/scenario_01.json donnees sortie.json
```

Dépendances : **pytest**, installation : python -m pip install pytest

## Tester

Commande de test : 
```
python -m pytest -v
```

Ces tests ne couvrent pour l'instant que des erreurs lors de la désérialisation d'une carte
Pour l'instant il n'y a pas de tests pour la désérialisation des autres formats de json, parce que c'est exactement le même principe et c'est pas ce qui est intéressant dans le projet.

## Organisation du code

| Fichier | Rôle |
|---|---|
| `Projet.py` | point d'entrée, lancement de la simulation|
| `Simulation.py` | simulation générale, possède la carte, l'armoire, le dictionnaire, le(s) robot(s) (lors de la suite du projet) |
| `Robot.py` | Agent, possède une mémoire (ses attributs), observe son environnement (avec des appels à la simulation), prend des décisions (implémenté comme une machine à état) |
| `…` | … |

## État

**Ce qui marche.** *À compléter.*

**Ce qui ne marche pas.** *À compléter — soyez honnêtes, c'est noté en
votre faveur.*

## Vidéo

`demo.mp4` (ou le lien), également déclarée dans `rendu.json`.
