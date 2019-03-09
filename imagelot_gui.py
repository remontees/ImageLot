#!/usr/bin/env python3
#coding: utf8
"""
Module principal permettant l'implémentation de l'interface graphique
du programme ImageLot

Dépendances : librairie PyQt, json

"""
import sys
import json
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget, \
                            QFormLayout, QPushButton, QFontDialog, QFileDialog, QColorDialog, \
                            QSpinBox, QCheckBox, QAction, QLabel, QFrame, QMessageBox,\
                            QComboBox, QErrorMessage, QLineEdit, qApp
from utils import pretty_list
from imagelot_process import process_json, batch_processing

class Form(QWidget):
    """ Classe représentant le formulaire complet.

    """
    def __init__(self):
        """ Constructeur du formulaire

        """
        super().__init__()
        self.files = []
        self.border_color = QColor(0, 0, 0)
        self.text_color = QColor(0, 0, 0)
        self.border_width = 1
        self.font_editor = None
        self.url_watermark = ""

        try:
            parameters_file = open("parameters.json", 'r')
            self.parameters = process_json(parameters_file)
            parameters_file.close()
        except IOError:
            self.parameters = {} # En cas de souci

        print(self.parameters)

        self.dest = ""
        self.run_main()

    def show_files_dialog(self):
        """ Affichage de la fenêtre de sélection des photos à traiter

        """
        file_dialog = QFileDialog().getOpenFileNames(self, "Choisir des images",\
                                                     "", "Photos (*.jpg *.png *.gif)")

        self.files = file_dialog[0]
        self.line_img.setText(pretty_list(file_dialog[0]))

    def show_file_dialog(self):
        """ Affichage de la fenêtre de sélection du watermark

        """
        file_dialog = QFileDialog().getOpenFileName(self, "Choisir une image",\
                                                     "", "Photos (*.jpg *.png *.gif)")

        self.url_watermark = file_dialog[0]
        self.line_watermark.setText(file_dialog[0])

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
            self.color_btn.setStyleSheet("QWidget { background-color: %s }"\
            % self.border_color.name())

    def show_textcolor_dialog(self):
        """ Affichage de la fenêtre de sélection de la couleur du texte

        """
        self.text_color = QColorDialog().getColor()

        if self.text_color.isValid():
            self.color_btn_txt.setStyleSheet("QWidget { background-color: %s }"\
            % self.text_color.name())

    def show_font_dialog(self):
        """ Affichage de la fenêtre de mise en forme du texte

        """
        if self.font_editor is not None:
            self.font_editor, valid_load = QFontDialog(self.font_editor).getFont()
        else:
            self.font_editor, valid_load = QFontDialog().getFont()

        if valid_load:
            self.font_label.setText(self.font_editor.family())
            self.font_label.setFont(self.font_editor)

    def disable_border(self):
        """ Choisit ou non de rendre inactif la partie "choix de bordure"

        """
        if self.set_border.isChecked():
            self.border_width.setDisabled(False)
            self.color_btn.setDisabled(False)
        else:
            self.border_width.setDisabled(True)
            self.color_btn.setDisabled(True)

    def disable_redim(self):
        """ Choisit ou non de rendre inactif la partie "redimensionnement"

        """
        if self.set_redim.isChecked():
            self.width.setDisabled(False)
            self.height.setDisabled(False)
        else:
            self.width.setDisabled(True)
            self.height.setDisabled(True)

    def disable_copyright(self):
        """ Choisit ou non de rendre inactif la partie "copyright"

        """
        if self.set_copyright.isChecked():
            self.text_copyright.setDisabled(False)
            self.font_button.setDisabled(False)
            self.color_btn_txt.setDisabled(False)
            self.comboh_text.setDisabled(False)
            self.combov_text.setDisabled(False)
        else:
            self.text_copyright.setDisabled(True)
            self.font_button.setDisabled(True)
            self.color_btn_txt.setDisabled(True)
            self.comboh_text.setDisabled(True)
            self.combov_text.setDisabled(True)

    def disable_watermark(self):
        """ Choisit ou non de rendre inactif la partie "watermark"

        """
        if self.set_watermark.isChecked():
            self.comboh_watermark.setDisabled(False)
            self.combov_watermark.setDisabled(False)
            self.line_watermark.setDisabled(False)
            self.browse_watermark_button.setDisabled(False)
        else:
            self.comboh_watermark.setDisabled(True)
            self.combov_watermark.setDisabled(True)
            self.line_watermark.setDisabled(True)
            self.browse_watermark_button.setDisabled(True)

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

        if self.set_border.isChecked():
            self.parameters["border"] = {}
            self.parameters["border"]["color"] = self.border_color.name()
            self.parameters["border"]["width"] = int(self.border_width.value())
        else:
            if "border" in self.parameters:
                del self.parameters["border"]

        if self.set_redim.isChecked():
            self.parameters["size"] = [self.width.value(), self.height.value()]
        else:
            if "size" in self.parameters:
                del self.parameters["size"]

        if self.set_copyright.isChecked():
            self.parameters["copyright"] = {}
            self.parameters["copyright"]["text"] = self.text_copyright.text()
            self.parameters["copyright"]["font"] = [self.font_editor.family(),
                                                    self.font_editor.pointSize()]

            # Spécification des positionnements
            self.parameters["copyright"]["coords"] = [None, None]

            if self.comboh_text.currentText() == "À gauche":
                self.parameters["copyright"]["coords"][0] = "gauche"
            elif self.comboh_text.currentText() == "Centré":
                self.parameters["copyright"]["coords"][0] = "centre"
            else:
                self.parameters["copyright"]["coords"][0] = "droite"

            if self.combov_text.currentText() == "En haut":
                self.parameters["copyright"]["coords"][1] = "haut"
            elif self.combov_text.currentText() == "Centré":
                self.parameters["copyright"]["coords"][1] = "centre"
            else:
                self.parameters["copyright"]["coords"][1] = "bas"

            self.parameters["copyright"]["color"] = self.text_color.name()
        else:
            if "copyright" in self.parameters:
                del self.parameters["copyright"]

        if self.set_watermark.isChecked():
            self.parameters["watermark"] = {}
            self.parameters["watermark"]["url"] = self.url_watermark

            # Spécification des positionnements
            self.parameters["watermark"]["coords"] = [None, None]

            if self.comboh_watermark.currentText() == "À gauche":
                self.parameters["watermark"]["coords"][0] = "gauche"
            elif self.comboh_watermark.currentText() == "Centré":
                self.parameters["watermark"]["coords"][0] = "centre"
            else:
                self.parameters["watermark"]["coords"][0] = "droite"

            if self.combov_watermark.currentText() == "En haut":
                self.parameters["watermark"]["coords"][1] = "haut"
            elif self.combov_watermark.currentText() == "Centré":
                self.parameters["watermark"]["coords"][1] = "centre"
            else:
                self.parameters["watermark"]["coords"][1] = "bas"
        else:
            if "watermark" in self.parameters:
                del self.parameters["watermark"]

        # Enregistrement des paramètres pour une prochaine exécution
        with open("parameters.json", "w") as parameters_file:
            parameters_file.write(self.get_parameters_json())

        # Traitement par lot

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

        ## REDIMENSIONNEMENT
        self.set_redim = QCheckBox()
        self.set_redim.stateChanged.connect(self.disable_redim)
        form_layout.addRow("&Redimensionner :", self.set_redim)

        self.width = QSpinBox()
        self.width.setRange(1, 50000)
        self.width.setSuffix(" px")
        self.height = QSpinBox()
        self.height.setRange(1, 50000)
        self.height.setSuffix(" px")
        self.width.setDisabled(True)
        self.height.setDisabled(True)
        form_layout.addRow("&Nouvelle largeur (format \"paysage\") :", self.width)
        form_layout.addRow("N&ouvelle hauteur (format \"portrait\") :", self.height)

        if "size" in self.parameters:
            self.set_redim.setChecked(2)
            self.disable_redim()

            if self.parameters["size"] is not None and len(self.parameters["size"]) == 2:
                self.width.setValue(int(self.parameters["size"][0]))
                self.height.setValue(int(self.parameters["size"][1]))

        ## BORDURES
        separateur2 = QFrame()
        separateur2.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur2)

        self.set_border = QCheckBox()
        self.set_border.stateChanged.connect(self.disable_border)
        form_layout.addRow("&Ajouter une bordure :", self.set_border)

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

        if "border" in self.parameters:
            self.set_border.setChecked(2)
            self.disable_border()

            if "width" in self.parameters["border"]:
                self.border_width.setValue(int(self.parameters["border"]["width"]))
            if "color" in self.parameters["border"]:
                self.color_btn.setStyleSheet("QWidget { background-color: %s }" % self.parameters["border"]["color"])
                self.border_color = QColor(self.parameters["border"]["color"])

        ## COPYRIGHT
        separateur3 = QFrame()
        separateur3.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur3)

        self.set_copyright = QCheckBox()
        self.set_copyright.stateChanged.connect(self.disable_copyright)
        form_layout.addRow("&Ajouter un copyright :", self.set_copyright)

        self.text_copyright = QLineEdit()
        form_layout.addRow("&Texte :", self.text_copyright)
        self.text_copyright.setDisabled(True)

        font_widget = QWidget()
        hbox_font = QHBoxLayout()
        hbox_font.addWidget(QLabel("Mise en forme :"))
        self.font_label = QLabel("Pas de mise en forme")
        self.font_button = QPushButton("Édition")
        hbox_font.addWidget(self.font_label)
        hbox_font.addWidget(self.font_button)

        self.font_button.clicked.connect(self.show_font_dialog)
        font_widget.setLayout(hbox_font)
        self.font_button.setDisabled(True)
        form_layout.addRow(font_widget)

        self.color_btn_txt = QPushButton()
        self.color_btn_txt.clicked.connect(self.show_textcolor_dialog)
        self.color_btn_txt.setStyleSheet("QWidget { background-color: %s }" % self.text_color.name())
        self.color_btn_txt.setDisabled(True)

        form_layout.addRow("&Couleur du texte :", self.color_btn_txt)

        self.comboh_text = QComboBox()
        self.comboh_text.addItem("À gauche")
        self.comboh_text.addItem("Centré")
        self.comboh_text.addItem("À droite")
        self.comboh_text.setDisabled(True)

        form_layout.addRow("&Positionnement horizontal :", self.comboh_text)

        self.combov_text = QComboBox()
        self.combov_text.addItem("En haut")
        self.combov_text.addItem("Centré")
        self.combov_text.addItem("En bas")
        self.combov_text.setDisabled(True)

        form_layout.addRow("&Positionnement vertical :", self.combov_text)

        if "copyright" in self.parameters:
            self.set_copyright.setChecked(2)
            self.disable_copyright()

            if "text" in self.parameters["copyright"]:
                self.text_copyright.setText(self.parameters["copyright"]["text"])
            if "color" in self.parameters["copyright"]:
                self.color_btn_txt.setStyleSheet("QWidget { background-color: %s }" % self.parameters["copyright"]["color"])
                self.text_color = QColor(self.parameters["copyright"]["color"])
            if "font" in self.parameters["copyright"]:
                self.font_editor = QFont(self.parameters["copyright"]["font"][0], self.parameters["copyright"]["font"][1])
                self.font_label.setText(self.font_editor.family())
                self.font_label.setFont(self.font_editor)
            if "coords" in self.parameters["copyright"]:
                if self.parameters["copyright"]["coords"][0] == "gauche":
                    self.comboh_text.setCurrentIndex(0)
                elif self.parameters["copyright"]["coords"][0] == "centre":
                    self.comboh_text.setCurrentIndex(1)
                elif self.parameters["copyright"]["coords"][0] == "droite":
                    self.comboh_text.setCurrentIndex(2)

                if self.parameters["copyright"]["coords"][1] == "haut":
                    self.combov_text.setCurrentIndex(0)
                elif self.parameters["copyright"]["coords"][1] == "centre":
                    self.combov_text.setCurrentIndex(1)
                elif self.parameters["copyright"]["coords"][1] == "bas":
                    self.combov_text.setCurrentIndex(2)


        ## AJOUTER WATERMARK
        separateur4 = QFrame()
        separateur4.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur4)

        self.set_watermark = QCheckBox()
        self.set_watermark.stateChanged.connect(self.disable_watermark)
        form_layout.addRow("&Ajouter un watermark :", self.set_watermark)

        watermark_widget = QWidget()
        hbox_img_watermark = QHBoxLayout()
        hbox_img_watermark.addWidget(QLabel("Watermark :"))
        self.line_watermark = QLineEdit()
        self.line_watermark.setReadOnly(True)
        self.browse_watermark_button = QPushButton("&Parcourir...")
        hbox_img_watermark.addWidget(self.line_watermark)
        hbox_img_watermark.addWidget(self.browse_watermark_button)

        self.browse_watermark_button.clicked.connect(self.show_file_dialog)
        watermark_widget.setLayout(hbox_img_watermark)
        self.line_watermark.setDisabled(True)
        self.browse_watermark_button.setDisabled(True)

        form_layout.addRow(watermark_widget)

        self.comboh_watermark = QComboBox()
        self.comboh_watermark.addItem("À gauche")
        self.comboh_watermark.addItem("Centré")
        self.comboh_watermark.addItem("À droite")
        self.comboh_watermark.setDisabled(True)

        form_layout.addRow("&Positionnement horizontal :", self.comboh_watermark)

        self.combov_watermark = QComboBox()
        self.combov_watermark.addItem("En haut")
        self.combov_watermark.addItem("Centré")
        self.combov_watermark.addItem("En bas")
        self.combov_watermark.setDisabled(True)

        form_layout.addRow("&Positionnement vertical :", self.combov_watermark)

        if "watermark" in self.parameters:
            self.set_watermark.setChecked(2)
            self.disable_watermark()

            if "url" in self.parameters["watermark"]:
                self.line_watermark.setText(self.parameters["watermark"]["url"])
                self.url_watermark = self.parameters["watermark"]["url"]
            if "coords" in self.parameters["watermark"]:
                if self.parameters["watermark"]["coords"][0] == "gauche":
                    self.comboh_watermark.setCurrentIndex(0)
                elif self.parameters["watermark"]["coords"][0] == "centre":
                    self.comboh_watermark.setCurrentIndex(1)
                elif self.parameters["watermark"]["coords"][0] == "droite":
                    self.comboh_watermark.setCurrentIndex(2)

                if self.parameters["watermark"]["coords"][1] == "haut":
                    self.combov_watermark.setCurrentIndex(0)
                elif self.parameters["watermark"]["coords"][1] == "centre":
                    self.combov_watermark.setCurrentIndex(1)
                elif self.parameters["watermark"]["coords"][1] == "bas":
                    self.combov_watermark.setCurrentIndex(2)

        ## DOSSIER DESTINATION
        separateur5 = QFrame()
        separateur5.setFrameStyle(QFrame.HLine | QFrame.Raised)
        form_layout.addRow(separateur5)

        dest_widget = QWidget()
        hbox_dest = QHBoxLayout()
        hbox_dest.addWidget(QLabel("Dossier d'enregistrement :"))
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
        return json.dumps(self.parameters, sort_keys=True, indent=4)


class Fenetre(QMainWindow):
    """ Classe représentant la fenêtre principale.
    Hérite de QWidget.

    """
    def __init__(self):
        """ Constructeur de la fenêtre par héritage de QWidget

        """
        super().__init__()
        self.run_main()

    def about(self):
        """ Une petite fenêtre d'informations à propos

        """
        QMessageBox.about(self, "ImageLot",
                          "Application de traitement par lot de photos réalisée en Python3 à l'aide\ndes librairies Pillow et PyQt5.\nPartagé sous licence libre GPL-3.0.\n\nAuteur : remontees (2017-2019).")

    def run_main(self):
        """ Configuration de la fenêtre principale

        """
        exit_action = QAction('&Quitter', self)
        exit_action.setText("&Quitter")
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("Quitter ImageLot")
        exit_action.triggered.connect(qApp.exit)

        about_action = QAction('À &propos', self)
        about_action.triggered.connect(self.about)

        menu = self.menuBar()
        menu_fichier = menu.addMenu("&Fichier")
        menu_fichier.addAction(exit_action)
        menu_fichier.addAction(about_action)

        form_widget = Form()

        self.setCentralWidget(form_widget)

        self.setGeometry(300, 300, 700, 400)
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
