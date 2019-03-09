#!/usr/bin/env python3
#coding: utf8
"""Fichier d'installation de nos scripts ImageLot CLI et GUI"""

from cx_Freeze import setup, Executable

# Définition du setup
setup(
    name = "ImageLot",
    version = "0.1",
    description = "Traitement par lot d'images simple et rapide",
    executables = [Executable("imagelot_cli.py"), Executable("imagelot_gui.py")],
)
