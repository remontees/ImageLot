ImageLot, un logiciel de traitement par lots de photos simple
=============================================================

Dépendances
-----------

Codé en Python, utilise Pillow (Python Imaging Library maintenu pour Python3).

La version par interface graphique utilisant GTK+3 est pour le moment abandonnée.



Fonctionnalités
-----------

EN COURS DE DEVELOPPEMENT


Permettra par ligne de commande (puis interface graphique) de faire différentes opérations de traitement par lot sur des photos :

* Redimensionnement
* Ajout de bordures
* Ajout de textes
* Ajout d'images (logos) en watermark (à terme)

Utilisation en ligne de commande (CLI)
--------------------------------------

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

Les opérations à effectuer sur le lot d'images sont à spécifier dans un fichier `JSON` dont vous passerez l'adresse en paramètre `-p` ou `--parameters` à ImageLot. Voici un exemple de configuration `JSON` pour ImageLot :

```json
{
    "size": [900, 900],
    "border": {
        "color": "black",
        "width": 3
    }
}
```
