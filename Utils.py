#!/usr/bin/env python3
#coding: utf8

"""Module destiné à offrir des fonctions de calcul pour les opérations
sur les images
et sur l'interface graphique

"""
def calcul_bordure(longueur_cote, largeur_bordure):
    """Fonction retournant la largeur d'une image avec la bordure ajoutée

    """
    return longueur_cote+2*largeur_bordure
