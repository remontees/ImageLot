#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant la lecture des paramètres et le traitement par lot

Dépendances externes : json, sys
"""
import json
import sys
from photo import Photo

def process_json(json_file):
    """
    Fonction assurant la lecture des paramètres de traitement par lot JSON.
    """
    try:
        parameters = json.loads(json_file)
    except json.JSONDecodeError:
        sys.stderr.write("Impossible d'extraire les paramètres\
         du fichier {}.\n".format(json_file.name))
        sys.exit(1)

    return parameters

def batch_processing(files, parameters, dest):
    """
    Fonction assurant le traitement par lot
    """
    for url_photo in files:
        file = Photo(url_photo)
        # traitement photo
