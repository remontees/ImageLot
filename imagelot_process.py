#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant la lecture des paramètres et le traitement par lot

"""
import json
import sys
import threading
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

    return parameters

def traitement(url_photo, parameters, dest):
    """
    Fonction assurant le traitement pour une photo
    """
    file = Photo(url_photo, dest)
    # traitement photo
    if "size" in parameters:
        file.redimensionner(*parameters["size"])

    file.sauvegarder()

def batch_processing(files, parameters, dest):
    """
    Fonction assurant le traitement par lot en parallèle !!
    """
    threads = [threading.Thread(target=traitement(url_photo, parameters, dest)) \
               for url_photo in files]

    # On lance nos threads en parallèle
    for thread in threads:
        thread.start()

    # On attend qu'ils terminent
    for thread in threads:
        thread.join()

    print("\nTraitement par lot terminé !")
