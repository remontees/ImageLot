#!/usr/bin/env python3
#coding: utf8

"""Module destiné à offrir des fonctions de calcul pour les opérations
sur les images
et sur l'interface graphique

"""
from PIL import Image
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
            if image_ouverte.format not in ("JPEG", "PNG", "GIF"):
                raise TypeError("Le format de l'image doit être en JPEG, PNG ou GIF.")
            else:
                return image_ouverte
    else:
        raise IOError("Il faut donner une URL de photo pour instancier l'objet.")

def create_img_chooser(title, multiple=False):
    """
    Fonction permettant de générer une fenêtre et un bouton pour sélectionner des
    images

    """
    dialog = Gtk.FileChooserDialog(title,
                                   None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    filter_img = Gtk.FileFilter()
    filter_img.set_name(("Images (jpg, png et gif)"))
    filter_img.add_mime_type("image/jpeg")
    filter_img.add_mime_type("image/png")
    filter_img.add_mime_type("image/gif")
    filter_img.add_pattern("*.jpe?g")
    filter_img.add_pattern("*.png")
    filter_img.add_pattern("*.gif")

    dialog.add_filter(filter_img)
    dialog.set_select_multiple(multiple)
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_action(Gtk.FileChooserAction.OPEN)
    file_chooser = Gtk.FileChooserButton.new_with_dialog(dialog)
    file_chooser.set_title(title)
    return file_chooser
