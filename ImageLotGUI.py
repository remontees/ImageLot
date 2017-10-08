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
from GUIUtils import create_img_chooser, create_position_chooser

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

    file_chooser = create_img_chooser("Sélectionnez les photos à traiter par lot", window, True)
    main_grid.attach(file_chooser, 1, 1, 1, 1)

    # Sélection du fichier à rajouter sur la photo
    label_watermark = Gtk.Label("Ajouter une image sur les photos : ")
    main_grid.attach(label_watermark, 0, 2, 1, 1)

    watermark_chooser = create_img_chooser("Sélectionner un logo à poser sur chaque photo", window)
    main_grid.attach(watermark_chooser, 1, 2, 1, 1)

    boxposition = create_position_chooser()
    main_grid.attach(boxposition, 1, 3, 1, 1)

    label_img_align = Gtk.Label("Alignement de l'image à apposer : ")
    main_grid.attach(label_img_align, 0, 3, 1, 1)

    button_save = Gtk.Button(label="Exécuter les actions")
    main_grid.attach(button_save, 0, 1000, 1, 1)

    window.add(main_grid)

    window.show_all()
    Gtk.main()

# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_gui()
