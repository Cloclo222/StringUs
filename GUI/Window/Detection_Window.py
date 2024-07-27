from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc
import serial.tools.list_ports


# Définition de la classe Window_GetName héritant de QWidget
class Window_Detection(QWidget):
    # Signal émis lorsqu'un nom de fichier est soumis
    submitted = qtc.pyqtSignal(str)

    # Initialisation de la classe
    def __init__(self, AutoDetectPort):
        super().__init__()  # Appel du constructeur de la classe mère QWidget
        self.setWindowTitle("Detection du port Arduino")  # Titre de la fenêtre

        self.port = AutoDetectPort  # Variable pour stocker le nom du fichier

        # Bouton "OK"
        self.EnregistrerButton = QPushButton("Enregistrer")
        self.EnregistrerButton.clicked.connect(
            self.EnregistrerButtonIsClicked)  # Connecte le clic du bouton à la méthode Ok_clique

        # Bouton "Cancel"
        self.canc_button = QPushButton("Cancel")
        self.canc_button.clicked.connect(self.canc_clique)  # Connecte le clic du bouton à la méthode canc_clique

        self.TestButton = QPushButton("Test")
        self.TestButton.clicked.connect(self.TestButtonClicked)  # Connecte le clic du bouton à la méthode canc_clique

        self.AutoDetectButton = QPushButton("Auto")
        self.AutoDetectButton.clicked.connect(self.AutoDetectButtonClicked)  # Connecte le clic du bouton à la méthode canc_clique

        self.PortBox = QSpinBox(minimum=1, maximum=12, value=1)
        self.PortBox.valueChanged.connect(self.PortBoxChange)
        self.PortBox.setMinimumHeight(40)
        font = self.PortBox.font()
        font.setPointSize(12)
        self.PortBox.setFont(font)

        self.instruction = QLabel("La detection a trouvé " + str(self.port))

        # Création d'une grille pour organiser les widgets
        layout = QGridLayout()
        layout.addWidget(QLabel("Port selectionné:"), 0, 0, 1, 2)  # Étiquette pour le champ de texte
        layout.addWidget(self.PortBox, 0, 1, 1, 2)  # Champ de texte

        layout.addWidget(self.TestButton, 0, 3)  # Bouton "OK"
        layout.addWidget(self.AutoDetectButton, 1, 3)  # Bouton "OK"

        layout.addWidget(QLabel("Detection automatique:"), 2, 0)  # Étiquette pour le champ de texte
        layout.addWidget(self.instruction, 2, 1, 3, 1)

        layout.addWidget(self.EnregistrerButton, 3, 0)  # Bouton "OK"
        layout.addWidget(self.canc_button, 3, 3)  # Bouton "Cancel"
        self.setLayout(layout)  # Applique le layout à la fenêtre

        self.detect_openRB150()


    # Méthode appelée lorsqu'on clique sur le bouton "OK"
    def EnregistrerButtonIsClicked(self):
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

    def PortBoxChange(self):
        self.port = self.PortBox.value()

    def TestButtonClicked(self):
        result = self.ping_openRB150(self.port)

    def AutoDetectButtonClicked(self):
        self.detect_openRB150()

    def detect_openRB150(self):
        """
        Detect if an openRB-150 is connected to the serial ports.
        """
        openRB150_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB Serial Device' in p.description  # Replace with the exact description
        ]

        if not openRB150_ports:
            return False
        else:
            self.port = openRB150_ports
            return f"openRB-150 found on port(s): {', '.join(openRB150_ports)}"

    def ping_openRB150(self, portNumberTest):
        """
            Check if an openRB-150 is connected to the specified port.
            """
        portTest = "COM" + str(portNumberTest)
        try:
            port_info = serial.tools.list_ports.comports()
            for port in port_info:
                if port.device == portTest:
                    if 'openRB-150' in port.description:  # Replace with the exact description if necessary
                        return True

            return False
        except serial.SerialException as e:
            return f"Error accessing port {portTest}: {e}"
