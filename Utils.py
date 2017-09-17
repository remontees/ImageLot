#!/usr/bin/env python3
#coding: utf8

"""Module destiné à offrir des fonctions de calcul pour les opérations
sur les images

"""
from PIL import Image

def calcul_bordure(longueur_cote, largeur_bordure):
    """Fonction retournant la largeur d'une image avec la bordure ajoutée

    """
    return longueur_cote+2*largeur_bordure

def ouvrir_photo(url_photo):
    """Fonction permettant d'ouvrir une photo avec PIL

    """
    if url_photo:
        with Image.open(url_photo) as image_ouverte:
            # Vérification du format de l'image
            if image_ouverte.format not in ("JPEG", "PNG", "BMP"):
                raise TypeError("Le format de l'image doit être en JPEG, PNG ou BMP.")
            else:
                return image_ouverte
    else:
        raise IOError("Il faut donner une URL de photo pour instancier l'objet.")
