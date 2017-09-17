#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant l'implémentation de l'interface graphique
du programme ImageLot

Dépendances : module Gtk

"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Utils import create_img_chooser

def main_gui():
    """
    Fonction permettant l'exécution du programme graphique associé à ImageLot

    """
    window = Gtk.Window()
    window.set_title("ImageLot - Traitement par lot d'images")
    window.set_default_size(640, 480)
    window.connect('delete-event', Gtk.main_quit)

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

# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_gui()
