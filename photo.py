#!/usr/bin/env python3
# coding: utf8
"""
Projet ImageLot
Module permettant de charger les photos
Utilise la librairie Pillow (fork de PIL pour Python3)
"""
from os.path import basename
import sys
from PIL import Image, ImageFont, ImageDraw
from utils import calcul_bordure, position_rel

class Photo:
    """ Classe permettant de manipuler une photo.
    Requiert l'utilisation du module Pillow

    """
    def __init__(self, url_photo, destination):
        """ Constructeur de la classe Photo
        Assure le chargement correct de la photo par Pillow

        """
        with Image.open(url_photo) as image_ouverte:
            # Vérification du format de l'image
            if image_ouverte.format not in ("JPEG", "PNG", "GIF", "MPO"):
                raise TypeError("Le format de l'image doit être en JPEG, PNG ou GIF.")

            # On copie la photo pour ne pas détériorer l'image originale
            coords_image_x = image_ouverte.size[0]
            coords_image_y = image_ouverte.size[1]
            coords_image = (coords_image_x, coords_image_y)
            self.name = basename(url_photo)
            self.image = Image.new(image_ouverte.mode, coords_image, "white")
            self.image.paste(image_ouverte, (0, 0, coords_image_x, coords_image_y))
            self.draw = ImageDraw.Draw(self.image)
            self.destination = destination

            # ATTENTION : On ferme l'image avant la fin de la construction de l'objet /!\
            image_ouverte.close()
            del image_ouverte

            # On ajoute les paramètres de taille de l'image à l'objet
            self.taille = [coords_image_x, coords_image_y]
            # On passe uniquement par l'objet maintenant
            self.mode_couleur = self.image.mode
            self.type_image = self.image.format

    def __del__(self):
        """Destruction de l'image lorsque l'objet est détruit afin d'éviter
        de garder des accès au disque dur.

        """
        try:
            try:
                if self.image and self.draw:
                    self.image.close()
                    del self.draw
            except AttributeError:
                sys.stderr.write("L'image n'a pas pu être fermée car elle n'a pas été ouverte.\n")
                sys.exit(1)
        except:
            raise GeneratorExit("La photo courante n'a pas pu être refermée correctement.")

    def __str__(self):
        """Fonction permettant de transformer l'image en chaine de caractères compréhensible

        """
        return self.name if self.name else None

    # Méthodes de manipulation des images
    def ajouter_bordure(self, epaisseur, couleur):
        """Ajoute une bordure colorée de l'épaisseur choisie à l'image courante.

        """
        nouvelle_largeur = calcul_bordure(self.taille[0], epaisseur)
        nouvelle_hauteur = calcul_bordure(self.taille[1], epaisseur)

        new_image = Image.new(self.mode_couleur, (nouvelle_largeur, nouvelle_hauteur), couleur)
        new_image.paste(self.image, (epaisseur, epaisseur))
        self.image = new_image

    def ajouter_texte(self, texte, font, coords, couleur):
        """Ajout d'un texte sur la photo
        Variable couleur est un triplet codant la couleur en RVB
        font est une paire (url_font, taille_font) pour les paramètres de police
        de caractère

        """
        self.draw = ImageDraw.Draw(self.image)
        url_font, taille_font = font

        try:
            font = ImageFont.truetype(url_font, taille_font)
        except (FileNotFoundError, OSError):
            sys.stderr.write("Chargement de la police d'écriture impossible.\n")
            sys.exit(1)

        text_size = list(self.draw.textsize(texte, font=font))

        # Définition des coordonnées relatives de positionnement du texte
        coords_txt = position_rel(coords, self)
        # Ajustement avec la taille du texte
        if coords[0] == "centre":
            coords_txt[0] -= text_size[0] // 2
        if coords[0] == "droite":
            coords_txt[0] -= text_size[0]
        if coords[1] == "bas":
            coords_txt[1] -= text_size[1]
        if coords[1] == "centre":
            coords_txt[1] -= text_size[1] // 2

        coords_txt = tuple(coords_txt)
        self.draw.text(coords_txt, texte, couleur, font=font)

    def ajouter_logo(self, logo_watermark, coords):
        """Ajout d'une image (type logo) en watermark sur l'image instanciée
        dans l'objet courant

        """
        # Définition des coordonnées relatives de positionnement du watermark
        coords_img = position_rel(coords, self)

        with Image.open(logo_watermark) as image_ouverte:
            # Vérification du format de l'image
            if image_ouverte.format not in ("JPEG", "PNG", "GIF"):
                raise TypeError("Le format de l'image doit être en JPEG, PNG ou GIF.")

            # Définition de la zone de collage en fonction de la taille du watermark
            if coords[0] == "centre":
                coords_img[0] -= image_ouverte.size[0] // 2
            if coords[0] == "droite":
                coords_img[0] -= image_ouverte.size[0]
            if coords[1] == "bas":
                coords_img[1] -= image_ouverte.size[1]
            if coords[1] == "centre":
                coords_img[1] -= image_ouverte.size[1] // 2

            self.image.paste(image_ouverte, tuple(coords_img), image_ouverte)

    # S'exécute uniquement en première fonction de traitement
    def redimensionner(self, largeur, hauteur):
        """Redimensionne une photo suivant les tailles données en paramètre
        tout en conservant le ratio de l'image d'origine

        """
        # On vérifie si les tailles fournies sont valides !!!
        assert isinstance(largeur, int) is True
        assert isinstance(hauteur, int) is True

        # Gestion du ratio
        ratio = self.taille[0] / self.taille[1]

        if self.taille[1] > self.taille[0]:
            largeur = int(hauteur*ratio)
        else:
            hauteur = int(largeur/ratio)

        self.taille = [largeur, hauteur]


        self.image = self.image.resize((largeur, hauteur), resample=Image.LANCZOS)

    def sauvegarder(self):
        """Sauvegarde l'image traitée sur le disque dur

        """
        self.image.save(self.destination + "/" + self.name)
        print("{} : OK.".format(self.name))
