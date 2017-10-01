#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant l'implémentation de l'interface graphique
du programme ImageLot

Dépendances : librairie Gtk

"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def main_gui():
    """
    Fonction permettant d'initialiser les paramètres de la fenêtre
    """
    # Définition des constantes de l'interface graphique
    nom_logiciel = "ImageLot"
    description_logiciel = "Traitement par lot d'images"
    width = 640
    height = 480

    window = Gtk.Window()
    window.set_title(nom_logiciel + " - " + description_logiciel)
    window.set_default_size(width, height)
    # Événément permettant d'assurer la fermeture correcte du logiciel
    window.connect('delete-event', Gtk.main_quit)

    # Définition de la grille de l'interface
    main_grid = Gtk.Grid()

    # Petit message d'accueil :-)
    label_home = Gtk.Label()
    label_home.set_markup('<b><span size="large">Bienvenue sur ImageLot !</span></b>')
    label_home.set_halign(Gtk.Align.START)
    main_grid.attach(label_home, 0, 0, 2, 1)

    # Sélection multiple des fichiers
    label_file = Gtk.Label("Sélectionnez les photos à traiter : ")
    label_file.set_halign(Gtk.Align.START)
    main_grid.attach(label_file, 0, 1, 1, 1)

    file_chooser = create_img_chooser("Sélectionnez les photos à traiter par lot", True)
    main_grid.attach(file_chooser, 1, 1, 1, 1)

    # Sélection du fichier à rajouter sur la photo
    label_watermark = Gtk.Label("Ajouter une image sur les photos : ")
    main_grid.attach(label_watermark, 0, 2, 1, 1)

    img_chooser = create_img_chooser("Sélectionner une image à apposer sur chaque photo")
    main_grid.attach(img_chooser, 1, 2, 1, 1)

    button_save = Gtk.Button(label="Exécuter les actions")
    main_grid.attach(button_save, 0, 1000, 1, 1)

    window.add(main_grid)

    window.show_all()
    Gtk.main()

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
    dialog.connect("response", callback_read_files)
    file_chooser = Gtk.FileChooserButton.new_with_dialog(dialog)
    file_chooser.set_title(title)
    return file_chooser

def callback_read_files(dialog, response_id):
    """
    Fonction de callback sur le chargement des fichiers
    """
    if response_id == Gtk.ResponseType.OK:
        print(dialog.get_filenames())
    elif response_id == Gtk.ResponseType.CANCEL:
        print("cancelled: FileChooserAction.OPEN")


# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_gui()
