#!/usr/bin/env python3
#coding: utf8
"""
Module implémentant les différentes fonctionnalités utiles de notre
interface graphique
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def create_img_chooser(title, window, multiple=False):
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
    # On regarde si les fichiers ont bien été trouvés
    try:
        dialog.connect("response", callback_read_files)
    except IOError as error:
        messagedialog = Gtk.MessageDialog(window,
                                          flags=Gtk.DialogFlags.MODAL,
                                          type=Gtk.MessageType.WARNING,
                                          buttons=Gtk.ButtonsType.OK_CANCEL,
                                          message_format=error.strerror)
        messagedialog.connect("response", callback_dialog_close)
        messagedialog.show()

    file_chooser = Gtk.FileChooserButton.new_with_dialog(dialog)
    file_chooser.set_title(title)
    return file_chooser

def create_position_chooser():
    """
    Créé une liste déroulante de choix de positonnement
    """
    tableau_positionnement = [['Haut/Gauche', 'hg'],
                              ['Haut/Centre', 'hc'],
                              ['Haut/Droite', 'hd'],
                              ['Milieu/Gauche', 'cg'],
                              ['Au centre', 'cc'],
                              ['Milieu/Droite', 'cd'],
                              ['Bas/Gauche', 'bg'],
                              ['Bas/Centre', 'bc'],
                              ['Bas/Droite', 'bd']
                             ]
    boxposition = Gtk.ComboBoxText()
    for position in tableau_positionnement:
        boxposition.append(position[1], position[0])
    boxposition.set_active(0)
    return boxposition

def callback_read_files(dialog, response_id):
    """
    Fonction de callback sur le chargement des fichiers
    """
    if response_id == Gtk.ResponseType.OK:
        return dialog.get_filenames()
    elif response_id == Gtk.ResponseType.CANCEL:
        raise IOError("cancelled: FileChooserAction.OPEN")

def callback_dialog_close(widget, response_id):
    """
    Fonction de callback permettant de fermer les boîtes de dialogue
    """
    if response_id == Gtk.ResponseType.OK:
        widget.destroy()
    else:
        raise SystemError("Une erreur inconnue est survenue.")
