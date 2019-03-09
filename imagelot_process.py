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
from utils import verif_coords

def process_json(json_file):
    """
    Fonction assurant la lecture des paramètres de traitement par lot JSON.
    """
    try:
        parameters = json.loads(json_file.read())
    except json.JSONDecodeError:
        sys.stderr.write("Impossible de lire les paramètres {}.\n".format(json_file.name))
        sys.exit(1)

    if "copyright" in parameters and "coords" in parameters["copyright"]:
        if not verif_coords(parameters["copyright"]["coords"]):
            sys.stderr.write("Positionnement du copyright invalide.\n")
            sys.exit(1)

    if "img_copyright" in parameters and "coords" in parameters["watermark"]:
        if not verif_coords(parameters["watermark"]["coords"]):
            sys.stderr.write("Positionnement du watermark invalide.\n")
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

    if "watermark" in parameters and \
       "url" in parameters["watermark"] and "coords" in parameters["watermark"]:
        file.ajouter_logo(parameters["watermark"]["url"], parameters["watermark"]["coords"])

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
