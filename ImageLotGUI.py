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
    window.connect('delete-event', Gtk.main_quit)

    window.show_all()
    Gtk.main()
