#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant l'utilisation d'ImageLot en CLI

Dépendances : argparse, os

"""
import argparse
import os
from imagelot_process import process_json, batch_processing

def main_cli():
    """
    Fonction permettant de lancer ImageLot en CLI.
    """
    # Parsage des arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("f",
                        nargs="*",
                        help="Photos à traiter")
    parser.add_argument("-p",
                        "--parameters",
                        nargs="?",
                        default=None,
                        required=True,
                        help="Fichier de paramètres de traitement par lot au format JSON.")
    parser.add_argument("-d",
                        "--dest",
                        nargs="?",
                        default=None,
                        help="Répertoire de destination.")
    args = parser.parse_args()

    # Vérifications des paramètres
    if args.parameters.split('.')[-1] != "json" and \
        args.parameters.split('.')[-1] != "JSON" and \
        not os.path.isfile(args.parameters):
        raise IOError("Les paramètres doivent être spécifiés au format JSON.")

    if not os.path.isdir(args.directory):
        raise IOError("Le répertoire de destination spécifié n'est pas valide.")

    parameters = process_json(args.parameters)
    batch_processing(args.f, parameters, args.dest)


# Si l'on exécute le fichier, on lance la fonction main_gui
if __name__ == '__main__':
    main_cli()
