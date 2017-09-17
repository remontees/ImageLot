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

def main_gui():
    """
    Fonction permettant l'exécution du programme graphique associé à ImageLot

    """
    window = Gtk.Window()
    window.set_title("ImageLot - Traitement par lot d'images")
    window.set_default_size(640, 480)
    window.connect('delete-event', Gtk.main_quit)

    main_grid = Gtk.Grid()

    label_home = Gtk.Label()
    label_home.set_markup('<b><span size="large">Bienvenue sur ImageLot !</span></b>')
    label_home.set_halign(Gtk.Align.START)
    main_grid.attach(label_home, 0, 0, 2, 1)

    label_file = Gtk.Label("Sélectionnez les photos à traiter : ")
    label_file.set_halign(Gtk.Align.START)
    main_grid.attach(label_file, 0, 1, 1, 1)

    dialog = Gtk.FileChooserDialog(("ImageLot - Sélectionnez les photos à traiter"),
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
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.set_action(Gtk.FileChooserAction.OPEN)
    dialog.set_select_multiple(True)
    file_chooser = Gtk.FileChooserButton.new_with_dialog(dialog)
    file_chooser.set_title("ImageLot - Sélectionnez les photos à traiter")


    main_grid.attach(file_chooser, 1, 1, 1, 1)

    window.add(main_grid)

    window.show_all()
    Gtk.main()

# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_gui()
