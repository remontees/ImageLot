#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant l'implémentation de l'interface graphique
du programme ImageLot

Dépendances : librairie PyQt, json

"""
import sys
import json
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, \
                            QFormLayout, QPushButton, QLineEdit, QFileDialog, QColorDialog, \
                            QSpinBox, QCheckBox, QAction, QLabel, QFrame, QMessageBox,\
                            QErrorMessage, qApp
from utils import pretty_list
from imagelot_process import batch_processing

class Form(QWidget):
    """ Classe représentant le formulaire complet.

    """
    def __init__(self):
        """ Constructeur du formulaire

        """
        super().__init__()
        self.files = []
        self.border_color = QColor(0, 0, 0)
        self.border_width = 1
        self.parameters = {} # Ce qui contiendra les paramètres à exporter
        self.dest = ""
        self.run_main()

    def show_files_dialog(self):
        """ Affichage de la fenêtre de sélection des photos à traiter

        """
        file_dialog = QFileDialog().getOpenFileNames(self, "Choisir des images",\
                                                     "", "Photos (*.jpg *.png *.gif)")

        self.files = file_dialog[0]
        self.line_img.setText(pretty_list(file_dialog[0]))

    def show_directory_dialog(self):
        """ Affichage de la fenêtre de sélection des photos à traiter

        """
        directory_dialog = QFileDialog().getExistingDirectory(self,
                                                              "Sélectionner",
                                                              "",
                                                              QFileDialog.ShowDirsOnly |
                                                              QFileDialog.DontResolveSymlinks)

        self.dest = directory_dialog
        self.line_dest.setText(directory_dialog)

    def show_bordercolor_dialog(self):
        """ Affichage de la fenêtre de sélection de la couleur de bordure

        """
        self.border_color = QColorDialog().getColor()

        if self.border_color.isValid():
            self.color_btn.setStyleSheet("QWidget { background-color: %s }"% self.border_color.name())

    def disable_border(self):
        """ Choisit ou non de rendre inactif la partie "choix de bordure"

        """
        if self.is_border.isChecked():
            self.border_width.setDisabled(False)
            self.color_btn.setDisabled(False)
        else:
            self.border_width.setDisabled(True)
            self.color_btn.setDisabled(True)

    def disable_redim(self):
        """ Choisit ou non de rendre inactif la partie "redimensionnement"

        """
        if self.is_redim.isChecked():
            self.width.setDisabled(False)
            self.height.setDisabled(False)
        else:
            self.width.setDisabled(True)
            self.height.setDisabled(True)

    def process_form(self):
        """ Effectue le chargement des données du formulaire puis l'exécution
        du traitement par lot

        """
        if not self.files:
            errorbox = QMessageBox()
            errorbox.setText("Aucune photo sélectionnée !")
            errorbox.setWindowTitle("Erreur")
            errorbox.exec_()
            return

        if self.dest == "":
            errorbox = QMessageBox()
            errorbox.setText("Merci de sélectionner un dossier d'enregistrement !")
            errorbox.setWindowTitle("Erreur")
            errorbox.exec_()
            return

        if self.is_border.isChecked():
            self.parameters["border"] = {}
            self.parameters["border"]["color"] = self.border_color.name()
            self.parameters["border"]["width"] = int(self.border_width.value())
        else:
            if "border" in self.parameters:
                del self.parameters["border"]

        if self.is_redim.isChecked():
            self.parameters["size"] = [self.width.value(), self.height.value()]
        else:
            if "size" in self.parameters:
                del self.parameters["size"]

        result = batch_processing(self.files, self.parameters, self.dest)

        msgbox = QMessageBox()
        msgbox.setText(result)
        msgbox.setWindowTitle("Traitement par lot terminé")
        msgbox.exec_()

    def run_main(self):
        """ Construit l'ensemble du formulaire

        """
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        file_widget = QWidget()

        hbox_img_files = QHBoxLayout()
        hbox_img_files.addWidget(QLabel("Photos :"))
        self.line_img = QLineEdit()
        self.line_img.setReadOnly(True)
        browse_button = QPushButton("&Parcourir...")
        hbox_img_files.addWidget(self.line_img)
        hbox_img_files.addWidget(browse_button)

        browse_button.clicked.connect(self.show_files_dialog)
        file_widget.setLayout(hbox_img_files)

        form_layout.addRow(file_widget)

        separateur1 = QFrame()
        separateur1.setFrameStyle(QFrame.HLine | QFrame.Raised)

        form_layout.addRow(separateur1)

        self.is_redim = QCheckBox()
        self.is_redim.stateChanged.connect(self.disable_redim)
        form_layout.addRow("&Redimensionner :", self.is_redim)

        ## REDIMENSIONNEMENT

        separateur2 = QFrame()
        separateur2.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur2)

        self.width = QSpinBox()
        self.width.setRange(1, 50000)
        self.width.setSuffix(" px")
        self.height = QSpinBox()
        self.height.setRange(1, 50000)
        self.height.setSuffix(" px")
        self.width.setDisabled(True)
        self.height.setDisabled(True)
        form_layout.addRow("&Nouvelle largeur :", self.width)
        form_layout.addRow("&Nouvelle hauteur :", self.height)

        ## BORDURES

        separateur3 = QFrame()
        separateur3.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur3)

        self.is_border = QCheckBox()
        self.is_border.stateChanged.connect(self.disable_border)
        form_layout.addRow("&Ajouter une bordure :", self.is_border)

        self.border_width = QSpinBox()
        self.border_width.setMinimum(1)
        self.border_width.setSuffix(" px")
        form_layout.addRow("&Taille de la bordure :", self.border_width)

        self.color_btn = QPushButton()
        self.color_btn.clicked.connect(self.show_bordercolor_dialog)
        self.color_btn.setStyleSheet("QWidget { background-color: %s }" % self.border_color.name())
        self.border_width.setDisabled(True)
        self.color_btn.setDisabled(True)

        form_layout.addRow("&Couleur de la bordure :", self.color_btn)

        ## DOSSIER DESTINATION

        separateur4 = QFrame()
        separateur4.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur4)

        dest_widget = QWidget()
        hbox_dest = QHBoxLayout()
        hbox_dest.addWidget(QLabel("Où enregistrer les photos traitées ?"))
        self.line_dest = QLineEdit()
        self.line_dest.setReadOnly(True)
        browse_dest_button = QPushButton("P&arcourir...")
        hbox_dest.addWidget(self.line_dest)
        hbox_dest.addWidget(browse_dest_button)

        browse_dest_button.clicked.connect(self.show_directory_dialog)
        dest_widget.setLayout(hbox_dest)
        form_layout.addRow(dest_widget)

        main_layout.addLayout(form_layout)

        btn_valider = QPushButton("&Exécuter les tâches")
        btn_valider.clicked.connect(self.process_form)
        main_layout.addStretch(1)
        main_layout.addWidget(btn_valider)

        self.setLayout(main_layout)

    def get_parameters_json(self):
        """ Retourne les paramètres du traitement par lot au format JSON.

        """
        return json.dumps(self.parameters)


class Fenetre(QMainWindow):
    """ Classe représentant la fenêtre principale.
    Hérite de QWidget.

    """
    def __init__(self):
        """ Constructeur de la fenêtre par héritage de QWidget

        """
        super().__init__()
        self.run_main()

    def run_main(self):
        """ Configuration de la fenêtre principale

        """
        exit_action = QAction('&Exit', self)
        exit_action.setText("&Quitter")
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("Quitter ImageLot")
        exit_action.triggered.connect(qApp.exit)

        menu = self.menuBar()
        menu_fichier = menu.addMenu("&Fichier")
        menu_fichier.addAction(exit_action)

        form_widget = Form()

        self.setCentralWidget(form_widget)

        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle("Traitement par lot - ImageLot")

        self.show()

def main(args):
    """Fonction permettant de démarrer la fenêtre graphique

    """
    application_courante = QApplication(sys.argv)
    window = Fenetre()
    sys.exit(application_courante.exec_())

if __name__ == "__main__":
    main(sys.argv)
