#!/usr/bin/env python3
# coding: utf8
"""
Projet ImageLot
Module permettant de charger les photos
Utilise la librairie PIL
"""
from PIL import Image, ImageFont, ImageDraw
from Utils import calcul_bordure

class Photo:
    """ Classe permettant de manipuler une photo.
    Requiert l'utilisation du module PIL

    """
    def __init__(self, url=None):
        """ Constructeur de la classe Photo
        Assure le chargement correct de la photo par PIL

        """
        if url:
            with Image.open(url) as image_ouverte:
                # Vérification du format de l'image
                if image_ouverte.format not in ("JPEG", "PNG", "BMP"):
                    raise TypeError("Le format de l'image doit être en JPEG, PNG ou BMP.")

                # On prépare les champs de l'objet
                self.type_image = self.image.format
                self.largeur = self.image.size[0]
                self.hauteur = self.image.size[1]
                self.mode_couleur = self.image.mode
                # On copie la photo pour ne pas détériorer l'image originale
                self.image = Image.new(self.mode_couleur, (self.largeur, self.hauteur), "white")
                self.image.paste(image_ouverte, (0, 0, self.largeur, self.hauteur))
                draw = ImageDraw.Draw(self.image)

    def __del__(self):
        """Destruction de l'image lorsque l'objet est détruit afin d'éviter
        de garder des accès au disque dur.

        """
        try:
            self.image.close()
        except:
            raise GeneratorExit("Le fichier courant n'a pas pu être refermé correctement.")

    # Méthodes de manipulation des images
    def ajouter_bordure(self, epaisseur, couleur):
        """Ajoute une bordure colorée de l'épaisseur choisie à l'image courante.

        """
        nouvelle_largeur = calcul_bordure(self.largeur, epaisseur)
        nouvelle_hauteur = calcul_bordure(self.hauteur, epaisseur)

        new_image = Image.new(self.mode_couleur, (nouvelle_largeur, nouvelle_hauteur, couleur))
        new_image.paste(self.image, (epaisseur, couleur))
        self.image = new_image

    def texte(self, texte, font, coords, couleur):
        """Ajout d'un texte sur la photo
        Variable couleur est un triplet codant la couleur en RVB
        font est une paire (url_font, taille_font) pour les paramètres de police
        de caractère

        """
        url_font, taille_font = font
        font = ImageFont.truetype(url_font, taille_font)
        draw.text(coords, texte, couleur, font=font)

        # S'exécute uniquement en première fonction de traitement
    def redimensionner(self, largeur, hauteur):
        """Redimensionne une photo suivant les tailles données en paramètre

        """
        pass

    def sauvegarder(self):
        """Sauvegarde l'image traitée sur le disque dur

        """
        self.image.save(self.type_image)
