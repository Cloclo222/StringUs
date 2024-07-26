import sys
import os
import cv2
import numpy as np
from PIL import Image

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIntValidator
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QSpinBox,
    QCheckBox, QMenuBar, QMenu, QAction, QMessageBox, QVBoxLayout, QHBoxLayout
)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Geometry of the page
        self.setWindowTitle("STRINGUS")
        self.setGeometry(50, 50, 800, 600)

        self.Titre = QLabel("STRINGUS: Du virtuel au réel")
        self.Titre.setFont(QFont('Arial', 30))
        self.Titre.setAlignment(Qt.AlignCenter)

        self.sous_titre = QLabel("Faites vos selections")
        self.sous_titre.setFont(QFont('Arial', 20))
        self.sous_titre.setAlignment(Qt.AlignCenter)

        # Create Menu
        self._createActions()
        self._createMenuBar()
        self._connectActions()

        # Global Variables
        self.fnameImage = 'Input/no.png'
        self.data_nbcouleur = 1
        self.rgb_values = []

        # Flags
        self.flag_calculate = False
        self.flag_browse = False
        self.flag_send = False
        self.flag_simulation = False
        self.flag_OpenCSV = False
        self.flag_sequenceCalculate = False

        # Default Parameters
        self.GreyScale = False
        self.defautpoid = 10
        self.defautep = 10
        self.sequencedefaut = ""
        self.sequence()
        self.sizedef = "Real"
        self.nbclous = 150
        self.diam = 500
        self.compteur = 0
        self.TotalNumberLines = 0
        self.offset = 0

        # Initialize UI components
        self.initUI()

    def initUI(self):
        # Box Nombre de clous
        self.ClousLine = QLineEdit(str(self.nbclous))
        self.ClousLine.setValidator(QIntValidator())
        self.ClousLine.setMaxLength(4)
        self.ClousLine.setAlignment(Qt.AlignLeft)
        self.ClousLine.setFont(QFont("Arial", 15))

        # Box Diametre
        self.DimLine = QLineEdit(str(self.diam))
        self.DimLine.setValidator(QIntValidator())
        self.DimLine.setMaxLength(3)
        self.DimLine.setAlignment(Qt.AlignLeft)
        self.DimLine.setFont(QFont("Arial", 15))

        # Browse Button
        BrowseButton = QPushButton("Browse")
        BrowseButton.clicked.connect(self.isBrowseButtonClick)
        BrowseButton.setMinimumHeight(40)
        BrowseButton.setFont(QFont("Arial", 15))
        self.image_path = QLabel("Vide")
        self.image_path.setMaximumWidth(299)

        # Calculate Button
        CalculateButton = QPushButton("Calculer")
        CalculateButton.clicked.connect(self.isCalculateButtonClick)
        CalculateButton.setMinimumHeight(50)
        CalculateButton.setFont(QFont("Arial", 15))

        # Send Button
        SendButton = QPushButton("Envoyer")
        SendButton.clicked.connect(self.isSendButtonClick)
        SendButton.setMinimumHeight(50)
        SendButton.setFont(QFont("Arial", 15))

        # Precedant Button
        PrecedantButton = QPushButton("Precedant")
        PrecedantButton.clicked.connect(self.isPrecedantButtonClick)
        PrecedantButton.setMinimumHeight(50)
        PrecedantButton.setFont(QFont("Arial", 15))

        # Simulation Button
        self.SimulationButton = QPushButton("Créer la simulation")
        self.SimulationButton.clicked.connect(self.isSimulationButtonClick)
        self.SimulationButton.setMinimumHeight(40)
        self.SimulationButton.setFont(QFont("Arial", 15))
        self.SimulationButton.setHidden(True)

        # Suivant Button
        NextButton = QPushButton("Suivant")
        NextButton.clicked.connect(self.isNextButtonClick)
        NextButton.setMinimumHeight(50)
        NextButton.setFont(QFont("Arial", 15))

        # Recalculate Sequence Button
        self.RecalculateSequenceButton = QPushButton("Recalculer avec nouvelle séquence")
        self.RecalculateSequenceButton.clicked.connect(self.isRecalculateSequenceButtonClick)
        self.RecalculateSequenceButton.setMinimumHeight(40)
        self.RecalculateSequenceButton.setFont(QFont("Arial", 15))
        self.RecalculateSequenceButton.setHidden(True)

        # Advanced Setting Button
        PAButton = QPushButton("Paramètre avancés")
        PAButton.clicked.connect(self.isPAButtonClick)
        PAButton.setFont(QFont("Arial", 15))

        # Nombre de couleur
        self.NbCouleurBox = QSpinBox()
        self.NbCouleurBox.setRange(1, 20)
        self.NbCouleurBox.setValue(1)
        self.NbCouleurBox.valueChanged.connect(self.isNbCouleurChange)
        self.NbCouleurBox.setMinimumHeight(40)
        self.NbCouleurBox.setFont(QFont("Arial", 12))

        # Image to print
        self.VOImage = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, 'C:\Users\Xavier Lefebvre\Documents\Université\test.png'))
        self.VOImage.setPixmap(self.pixmap)

        # Dominant Image
        self.DominantImage = QLabel()
        self.pixmap = QPixmap(self.resize_image(700, 300, 'C:\Users\Xavier Lefebvre\Documents\Université\test.png', 'C:\Users\Xavier Lefebvre\Documents\Université\test.png'))
        self.DominantImage.setPixmap(self.pixmap)

        # Preview Image
        self.PreviewImage = QLabel()
        pixmap = QPixmap(self.resize_image(400, 400, 'C:\Users\Xavier Lefebvre\Documents\Université\test.png', 'C:\Users\Xavier Lefebvre\Documents\Université\test.png'))
        self.PreviewImage.setPixmap(pixmap)

        # Check Box grey
        self.GreyBox = QCheckBox()
        self.GreyBox.setGeometry(QtCore.QRect(170, 120, 81, 20))
        self.GreyBox.stateChanged.connect(self.GreyBoxCheck)

        # Layouts
        main_layout = QVBoxLayout()
        title_layout = QVBoxLayout()
        title_layout.addWidget(self.Titre)
        title_layout.addWidget(self.sous_titre)

        input_layout = QGridLayout()
        input_layout.addWidget(QLabel("Nombre de clous:"), 0, 0)
        input_layout.addWidget(self.ClousLine, 0, 1)
        input_layout.addWidget(QLabel("Diametre (mm):"), 1, 0)
        input_layout.addWidget(self.DimLine, 1, 1)
        input_layout.addWidget(BrowseButton, 2, 0)
        input_layout.addWidget(self.image_path, 2, 1)
        input_layout.addWidget(QLabel("Nombre de couleur:"), 3, 0)
        input_layout.addWidget(self.NbCouleurBox, 3, 1)
        input_layout.addWidget(QLabel("Gris"), 4, 0)
        input_layout.addWidget(self.GreyBox, 4, 1)
        input_layout.addWidget(PAButton, 5, 0, 1, 2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(CalculateButton)
        button_layout.addWidget(SendButton)
        button_layout.addWidget(PrecedantButton)
        button_layout.addWidget(NextButton)
        button_layout.addWidget(self.RecalculateSequenceButton)
        button_layout.addWidget(self.SimulationButton)

        image_layout = QVBoxLayout()
        image_layout.addWidget(self.VOImage)
        image_layout.addWidget(self.DominantImage)
        image_layout.addWidget(self.PreviewImage)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(image_layout)

        self.setLayout(main_layout)

    def isSimulationButtonClick(self):
        self.flag_simulation = True
        self.canvas.animate(fps=60)
        QMessageBox.information(self, 'Simulation', "La simulation est prête et elle se trouve maintenant dans vos dossiers", QMessageBox.Ok)

    def isBrowseButtonClick(self):
        self.flag_browse = True
        self.flag_calculate = False
        self.flag_simulation = False

        self.transit = QFileDialog.getOpenFileName(self, 'Open file')
        self.fnameImage = self.transit[0]

        self.image_path.setText(self.fnameImage)
        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, 'Input/no.png'))
        self.VOImage.setPixmap(self.pixmap)

    def isCalculateButtonClick(self):
        self.flag_calculate = True
        self.flag_browse = False
        self.flag_send = False
        self.flag_simulation = False
        self.flag_OpenCSV = False

        self.nbclous = int(self.ClousLine.text())
        self.diam = int(self.DimLine.text())
        self.data_nbcouleur = self.NbCouleurBox.value()
        self.GreyScale = self.GreyBox.isChecked()

        if self.flag_calculate:
            # Add your calculation logic here
            self.TotalNumberLines = 1000  # Example value
            QMessageBox.information(self, 'Calcul terminé', f'Le calcul est terminé avec {self.TotalNumberLines} lignes.', QMessageBox.Ok)

    def isSendButtonClick(self):
        self.flag_send = True
        # Add your sending logic here
        QMessageBox.information(self, 'Envoyé', "Le fichier a été envoyé avec succès.", QMessageBox.Ok)

    def isPrecedantButtonClick(self):
        self.flag_sequenceCalculate = False
        # Add logic for previous step
        QMessageBox.information(self, 'Précédent', "Retour à l'étape précédente.", QMessageBox.Ok)

    def isNextButtonClick(self):
        self.flag_sequenceCalculate = True
        # Add logic for next step
        QMessageBox.information(self, 'Suivant', "Passer à l'étape suivante.", QMessageBox.Ok)

    def isRecalculateSequenceButtonClick(self):
        self.flag_sequenceCalculate = True
        # Add logic for recalculating sequence
        QMessageBox.information(self, 'Recalculer', "La séquence a été recalculée.", QMessageBox.Ok)

    def isPAButtonClick(self):
        # Add logic for advanced settings
        QMessageBox.information(self, 'Paramètre avancés', "Ouvrir les paramètres avancés.", QMessageBox.Ok)

    def isNbCouleurChange(self):
        # Update the number of colors
        self.data_nbcouleur = self.NbCouleurBox.value()

    def GreyBoxCheck(self):
        self.GreyScale = self.GreyBox.isChecked()

    def resize_image(self, width, height, input_path, default_path):
        if os.path.exists(input_path):
            img = cv2.imread(input_path)
        else:
            img = cv2.imread(default_path)

        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
        output_path = 'Output/ResizedImage.png'
        cv2.imwrite(output_path, img)
        return output_path

    def sequence(self):
        self.sequencedefaut = "sequence"

    def _createActions(self):
        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)

    def _createMenuBar(self):
        menuBar = QMenuBar(self)

        fileMenu = QMenu('&File', self)
        fileMenu.addAction(self.exitAction)

        menuBar.addMenu(fileMenu)
        #self.layout().setMenuBar(menuBar)

    def _connectActions(self):
        self.exitAction.triggered.connect(self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
