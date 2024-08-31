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
    submitted3 = qtc.pyqtSignal(int)

    # Initialisation de la classe
    def __init__(self, AutoDetectPort):
        super().__init__()  # Appel du constructeur de la classe mère QWidget
        self.setWindowTitle("Detection du port Arduino")  # Titre de la fenêtre

        self.port = AutoDetectPort


        # Bouton "OK"
        self.EnregistrerButton = QPushButton("Enregistrer")
        self.EnregistrerButton.clicked.connect(
            self.EnregistrerButtonIsClicked)

        # Bouton "Cancel"
        self.canc_button = QPushButton("Cancel")
        self.canc_button.clicked.connect(self.canc_clique)

        self.TestButton = QPushButton("Test")
        self.TestButton.clicked.connect(self.TestButtonClicked)

        self.AutoDetectButton = QPushButton("Auto")
        self.AutoDetectButton.clicked.connect(
            self.AutoDetectButtonClicked)

        if self.port == -1:
            self.instruction = QLabel("Aucun port n'est disponible")
            self.PortBox = QSpinBox(minimum=1, maximum=12, value=1)

        else:
            self.instruction = QLabel("Actuellement connecté au port " + str(self.port))
            self.PortBox = QSpinBox(minimum=1, maximum=12, value=self.port)

        self.PortBox.valueChanged.connect(self.PortBoxChange)
        self.PortBox.setMinimumHeight(40)
        font = self.PortBox.font()
        font.setPointSize(12)
        self.PortBox.setFont(font)

        # Création d'une grille pour organiser les widgets
        layout = QGridLayout()
        layout.addWidget(QLabel("Port selectionné:"), 0, 0, 1, 2)  # Étiquette pour le champ de texte
        layout.addWidget(self.PortBox, 0, 1, 1, 2)  # Champ de texte

        layout.addWidget(self.TestButton, 0, 3)  # Bouton "OK"
        layout.addWidget(self.AutoDetectButton, 1, 3)  # Bouton "OK"

        layout.addWidget(QLabel("État:"), 2, 0)  # Étiquette pour le champ de texte
        layout.addWidget(self.instruction, 1, 1, 3, 1)

        layout.addWidget(self.EnregistrerButton, 3, 0)  # Bouton "OK"
        layout.addWidget(self.canc_button, 3, 3)  # Bouton "Cancel"
        self.setLayout(layout)  # Applique le layout à la fenêtre

    # Méthode appelée lorsqu'on clique sur le bouton "OK"
    def EnregistrerButtonIsClicked(self):

        if not self.ping_openRB150(self.port):
            QMessageBox.information(self, 'ERREUR', "Incapable de me connecter au port", QMessageBox.Ok)

        else:
            # Émet le signal "submitted" avec le texte du champ de texte et ferme la fenêtre
            self.submitted3.emit(self.port)
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
            if 'USB Serial Device' in p.description or 'Périphérique série USB' in p.description  # Replace with the exact description
        ]

        if not openRB150_ports:
            self.instruction.setText("La détection n'a rien trouvé " + str(self.port))
            return False
        else:
            self.port = self.extract_numbers_and_convert(openRB150_ports[0])
            self.instruction.setText("La détection a trouvé " + str(self.port))
            self.PortBox.setValue(self.port)
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
                    self.instruction.setText("Port détecté!")  # Replace with the exact description if necessary
                    return True
            self.instruction.setText("Port non détecté")
            return False
        except serial.SerialException as e:
            return f"Error accessing port {portTest}: {e}"

    def extract_numbers_and_convert(self, string):
        # Keep only the digits
        digits = ''.join([char for char in string if char.isdigit()])
        # Convert the string of digits to an integer
        return int(digits)
