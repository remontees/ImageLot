ImageLot, un logiciel de traitement par lots de photos simple
=============================================================

Dépendances
-----------

Codé en Python, utilise Pillow (Python Imaging Library maintenu pour Python3).

La version par interface graphique utilisant GTK+3 est pour le moment abandonnée.



Fonctionnalités
---------------

Permet par ligne de commande (puis interface graphique) de faire différentes opérations de traitement par lot sur des photos :

* Redimensionnement
* Ajout de bordures
* Ajout de textes
* Ajout d'images (logos) en watermark

Lancement du programme graphique
--------------------------------

Il suffit d'exécuter le fichier `imagelot_gui.py` (après lui avoir préalablement donné les droits d'exécution). Cette version graphique d'ImageLot est réalisée à l'aide de PyQt5.

Elle assure pour le moment uniquement les fonctionnalités suivantes :

* Redimensionnement
* Ajout de bordures

Utilisation en ligne de commande (CLI)
--------------------------------------

### Préambule

La version en ligne de commande d'ImageLot implémente toutes les fonctionnalités (contrairement à la version graphique pour le moment).

### Syntaxe d'utilisation en ligne de commande

```
usage: imagelot_cli.py [-h] -p [PARAMETERS] [-d [DEST]] [f [f ...]]

positional arguments:
  f                     Photos à traiter

optional arguments:
  -h, --help            show this help message and exit
  -p [PARAMETERS], --parameters [PARAMETERS]
                        Fichier de paramètres de traitement par lot au format
                        JSON.
  -d [DEST], --dest [DEST]
                        Répertoire de destination.
```

### Spécification des paramètres de traitement par lot (CLI)

Les opérations à effectuer sur le lot d'images sont à spécifier dans un fichier `JSON` dont vous passerez l'adresse en paramètre `-p` ou `--parameters` à ImageLot.

#### Exemple de configuration `JSON` pour un copyright texte

```json
{
    "size": [900, 900],
    "border": {
        "color": "black",
        "width": 3
    },
    "copyright": {
        "text": "© 2019 - remontees",
        "font": "Ubuntu",
        "coords": [0, 0],
        "color": "black"
    }
}
```

#### Exemple de configuration `JSON` pour un watermark

Où `copyright.png` est le watermark à appliquer aux photos dans le dossier courant d'exécution.
```json
{
    "size": [900, 900],
    "border": {
        "color": "black",
        "width": 3
    },
    "watermark": {
        "url": "copyright.png",
        "coords": ["gauche", "bas"]
    }
}
```

Tests
-----

J'ai pour le moment écrit quelques tests pour les modules `photo` et `utils`.
Les tests peuvent être exécutés avec `pytest-3` en utilisant la commande suivante à la racine du projet :
```bash
pytest-3 test_*.py
```
Pour obtenir la couverture des tests, vous pouvez utiliser `pytest-cov` à la racine du projet comme suit :
```bash
pytest-3 --cov=. --cov-report html test_*.py
```
Celui-ci génère un rapport `html` à l'adresse relative `htmlcov/index.html` par rapport à la racine du projet.
