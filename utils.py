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

def verif_coords(tab):
    """Fonction permettant de vérifier que le placement demandé est valide.

    """
    if tab[0] not in ("gauche", "centre", "droite") or tab[1] not in ("bas", "centre", "haut"):
        return False

    return True

def position_rel(tab, image):
    """Fonction transformant un positionnement relatif en positionnement
    par coordonnées absolues

    """
    coords = [0, 0]
    if tab[0] == "gauche":
        coords[0] = 8
    if tab[0] == "centre":
        coords[0] = image.taille[0] // 2
    if tab[0] == "droite":
        coords[0] = image.taille[0] - 5
    if tab[1] == "bas":
        coords[1] = image.taille[1] - 10
    if tab[1] == "centre":
        coords[1] = image.taille[1] // 2
    if tab[1] == "haut":
        coords[1] = 5

    return coords

def pretty_list(liste):
    """Affiche joliment une liste Python

    """
    # Cas liste vide
    if not liste:
        return ""

    # Cas liste non vide
    iterateur_liste = iter(liste)
    liste_finale = next(iterateur_liste)

    for element in iterateur_liste:
        liste_finale += ", " + element

    return liste_finale
