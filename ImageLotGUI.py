#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant l'implémentation de l'interface graphique
du programme ImageLot

Dépendances : librairie Gtk

"""
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from GUIUtils import create_img_chooser, create_position_chooser

def main_gui():
    """
    Fonction permettant d'initialiser les paramètres de la fenêtre
    """
    window = Gtk.Window()
    window.set_title("ImageLot - Traitement par lot d'images")
    window.set_default_size(640, 480)
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

    # Commenté pour laisser la possibilité de mettre en place un watermark
    # label_watermark_chooser = Gtk.Label("Logo en watermark : ")
    # label_watermark_chooser.set_halign(Gtk.Align.START)
    # main_grid.attach(label_watermark_chooser, 0, 3, 1, 1)
    #
    # watermark_chooser = create_img_chooser("Choisir un logo en watermark :", window)
    # main_grid.attach(watermark_chooser, 1, 3, 1, 1)

    # Texte et mise en forme du texte du copyright
    label_copyright_text = Gtk.Label("Texte de copyright :")
    label_copyright_text.set_halign(Gtk.Align.START)
    main_grid.attach(label_copyright_text, 0, 3, 1, 1)

    copyright_text = Gtk.Entry()
    copyright_text.set_max_length(250)
    copyright_text.set_text('© ' + str(datetime.now().year))
    main_grid.attach(copyright_text, 1, 3, 1, 1)

    label_copyright_font = Gtk.Label("Police d'écriture :")
    label_copyright_font.set_halign(Gtk.Align.START)
    main_grid.attach(label_copyright_font, 0, 4, 1, 1)

    copyright_font = Gtk.FontButton()
    main_grid.attach(copyright_font, 1, 4, 1, 1)

    boxposition = create_position_chooser()
    main_grid.attach(boxposition, 1, 5, 1, 1)

    label_text_align = Gtk.Label("Alignement du copyright sur la photo : ")
    label_text_align.set_halign(Gtk.Align.START)
    main_grid.attach(label_text_align, 0, 5, 1, 1)

    label_copyright = Gtk.CheckButton.new_with_label('Ajouter un copyright texte sur les photos : ')
    tab_components = [label_copyright_text, copyright_text, label_text_align, boxposition, \
    label_copyright_font, copyright_font]
    label_copyright.connect('toggled', callback_copyright, tab_components)
    label_copyright.set_active(True)
    main_grid.attach(label_copyright, 0, 2, 1, 1)

    button_save = Gtk.Button(label="Exécuter les actions")
    main_grid.attach(button_save, 0, 1000, 1, 1)

    window.add(main_grid)

    window.show_all()
    Gtk.main()

def callback_copyright(checkbox, tab_components):
    """
    Fonction de callback permettant d'afficher/masquer les éléments permettant de choisir
    le copyright texte à ajouter
    """
    if checkbox.get_active() is False:
        for component in tab_components:
            component.hide()
    else:
        for component in tab_components:
            component.show()

# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_gui()
