#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant la lecture des paramètres et le traitement par lot

"""
import json
import sys
import threading
import time
from photo import Photo

def process_json(json_file):
    """
    Fonction assurant la lecture des paramètres de traitement par lot JSON.
    """
    try:
        parameters = json.loads(json_file.read())
    except json.JSONDecodeError:
        sys.stderr.write("Impossible d'extraire les paramètres\
         du fichier {}.\n".format(json_file.name))
        sys.exit(1)

    if "copyright" in parameters and \
       "text" in parameters["copyright"] and \
       "font" in parameters["copyright"] and \
       "color" in parameters["copyright"] and \
       "coords" in parameters["copyright"]:
        if parameters["copyright"]["coords"][0] not in ("gauche", "centre", "droite") or \
           parameters["copyright"]["coords"][1] not in ("bas", "centre", "haut"):
            sys.stderr.write("Positionnement du copyright invalide.\n")
            sys.exit(1)

    return parameters

def traitement(url_photo, parameters, dest):
    """
    Fonction assurant le traitement pour une photo
    """
    file = Photo(url_photo, dest)
    # traitement photo
    if "size" in parameters:
        file.redimensionner(*parameters["size"])

    if "copyright" in parameters and \
       "text" in parameters["copyright"] and \
       "font" in parameters["copyright"] and \
       "color" in parameters["copyright"] and \
       "coords" in parameters["copyright"]:
        file.ajouter_texte(parameters["copyright"]["text"],
                           parameters["copyright"]["font"],
                           parameters["copyright"]["coords"],
                           parameters["copyright"]["color"])

    if "border" in parameters and "width" in parameters["border"] \
        and "color" in parameters["border"]:
        file.ajouter_bordure(parameters["border"]["width"], parameters["border"]["color"])

    file.sauvegarder()

def batch_processing(files, parameters, dest):
    """
    Fonction assurant le traitement par lot en parallèle !!
    """
    threads = [threading.Thread(target=traitement(url_photo, parameters, dest)) \
               for url_photo in files]

    debut = time.time()
    # On lance nos threads en parallèle
    for thread in threads:
        thread.start()

    # On attend qu'ils terminent
    for thread in threads:
        thread.join()
    fin = time.time()

    print("\nTraitement par lot terminé en {} s !".format(round(fin-debut, 5)))
