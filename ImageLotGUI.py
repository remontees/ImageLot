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
    window.set_default_size(640,480)
    window.connect('delete-event', Gtk.main_quit)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    label_home = Gtk.Label()
    label_home.set_markup('<b><span size="large">Bienvenue sur ImageLot !</span></b>')
    label_home.set_halign(Gtk.Align.START)
    box.pack_start(label_home, True, True, 0)

    sub_box_file = Gtk.Box(spacing=10)
    label_file = Gtk.Label("Sélectionnez les photos à traiter : ")
    label_file.set_halign(Gtk.Align.START)
    sub_box_file.pack_start(label_file, True, True, 0)

    file_chooser = Gtk.FileChooserButton()
    file_chooser.set_title("ImageLot - Sélectionnez les photos à traiter")
    sub_box_file.pack_start(file_chooser, True, True, 0)
    box.pack_start(sub_box_file, True, True, 0)

    window.add(box)

    window.show_all()
    Gtk.main()

# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_gui()
