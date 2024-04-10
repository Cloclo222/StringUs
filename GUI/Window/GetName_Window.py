from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc

# Définition de la classe Window_GetName héritant de QWidget
class Window_GetName(QWidget):
    # Signal émis lorsqu'un nom de fichier est soumis
    submitted = qtc.pyqtSignal(str)

    # Initialisation de la classe
    def __init__(self):
        super().__init__()  # Appel du constructeur de la classe mère QWidget
        self.setWindowTitle("Nom du fichier?")  # Titre de la fenêtre

        self.DataName = None  # Variable pour stocker le nom du fichier

        # Bouton "OK"
        self.Ok_button = QPushButton("OK")
        self.Ok_button.clicked.connect(self.Ok_clique)  # Connecte le clic du bouton à la méthode Ok_clique

        # Bouton "Cancel"
        self.canc_button = QPushButton("Cancel")
        self.canc_button.clicked.connect(self.canc_clique)  # Connecte le clic du bouton à la méthode canc_clique

        # Champ de texte pour saisir le nom du fichier
        self.Name = QLineEdit()
        self.Name.setMaxLength(15)  # Limite la longueur du texte à 15 caractères
        self.Name.setAlignment(Qt.AlignLeft)  # Alignement du texte à gauche
        self.Name.setFont(QFont("Arial", 10))  # Police de caractères et taille

        # Création d'une grille pour organiser les widgets
        layout = QGridLayout()
        layout.addWidget(QLabel("Nom du fichier:"), 0, 0)  # Étiquette pour le champ de texte
        layout.addWidget(self.Name, 0, 1)  # Champ de texte
        layout.addWidget(self.Ok_button, 1, 0)  # Bouton "OK"
        layout.addWidget(self.canc_button, 1, 1)  # Bouton "Cancel"
        self.setLayout(layout)  # Applique le layout à la fenêtre

    # Méthode appelée lorsqu'on clique sur le bouton "OK"
    def Ok_clique(self):
        # Vérifie si le champ de texte est vide
        if self.Name.text() == "":
            # Affiche un message d'erreur si le champ de texte est vide
            QMessageBox.information(self, 'ERREUR', "J'ai besoin d'un nom de fichier (;", QMessageBox.Ok)
        else:
            # Émet le signal "submitted" avec le texte du champ de texte et ferme la fenêtre
            self.submitted.emit(self.Name.text())
            self.close()

    # Méthode appelée lorsqu'on clique sur le bouton "Cancel"
    def canc_clique(self):
        # Ferme simplement la fenêtre sans émettre de signal
        self.close()
