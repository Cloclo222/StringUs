import sys
import cv2
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import matplotlib
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc

from PIL import Image
from .Crop_window1 import *

class Window_PA(QWidget):
    submitted2 = qtc.pyqtSignal(list, str, int, int, str)

    def __init__(self, number_of_color_set: int, filename, rgb_image, pd, ep, seq, sizedef, grey):
        super().__init__()
        # Geometrie
        self.setWindowTitle("Parametres avancés")
        self.setGeometry(100, 100, 500, 500)

        self.Titre = QLabel("STRINGUS: Du virtuel au réel")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Parametres avances")
        self.sous_titre.setFont(QFont('Arial', 20))

        # Variable
        self.nb_couleur = number_of_color_set
        self.image_a_imprimer = filename
        self.Realrgb = []
        self.Realrgb = rgb_image
        self.size = sizedef
        self.valueepaisseur = ep
        self.valuepoid = pd
        self.sequence = seq
        self.greyscale = grey
        self.temp = self.Realrgb.copy()

        # Box Epaisseur de la ligne
        self.EpaisseurLine = QLineEdit(str(ep))
        # self.epaisseur = QLineEdit()
        self.EpaisseurLine.setValidator(QIntValidator())
        self.EpaisseurLine.setMaxLength(4)
        self.EpaisseurLine.setAlignment(Qt.AlignLeft)
        self.EpaisseurLine.setFont(QFont("Arial", 10))

        # Box Poid de la ligne
        self.PoidLine = QLineEdit(str(pd))
        self.PoidLine.setValidator(QIntValidator())
        self.PoidLine.setMaxLength(4)
        self.PoidLine.setAlignment(Qt.AlignLeft)
        self.PoidLine.setFont(QFont("Arial", 10))

        # Check Box RealSize
        self.checkBox_Real = QCheckBox()
        self.checkBox_Real.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Real.stateChanged.connect(self.checkeReal)

        # Check Box Resize
        self.checkBox_Resize = QCheckBox()
        self.checkBox_Resize.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Resize.stateChanged.connect(self.checkeResize)

        if self.size == "Real":
            self.checkBox_Resize.setChecked(False)
            self.checkBox_Real.setChecked(True)

        else:
            self.checkBox_Resize.setChecked(True)
            self.checkBox_Real.setChecked(False)

        # Selection Couleur
        self.CouleurChoiceBox = QSpinBox(minimum=1, maximum=self.nb_couleur, value=1)
        self.CouleurChoiceBox.valueChanged.connect(self.isCouleurChoiceBoxChange)

        # Couleur Dominant_image
        self.DominantImage = QLabel()
        self.pixmap = QPixmap(
            self.resize_image(600, 200, 'Input/bar.jpg', 'Input/bar.jpg'))
        self.DominantImage.setPixmap(self.pixmap)

        # Image a imprimer
        self.Image = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.image_a_imprimer, 'Output/resize_image.png'))
        self.Image.setPixmap(self.pixmap)

        # Box ordre
        self.OrdreLine = QLineEdit(seq)
        # self.ordre.setMaxLength(1000)
        self.OrdreLine.setAlignment(Qt.AlignLeft)
        self.OrdreLine.setFont(QFont("Arial", 10))

        # Changement de couleur bouton
        self.ChangeColorButton = QPushButton("Changer la couleur")
        self.ChangeColorButton.clicked.connect(self.isChangeColorButtonPush)

        # Crop Button
        self.CropButton = QPushButton("Modifier l'image")
        self.CropButton.clicked.connect(self.isCropButtonPush)

        # Enregistrer Button
        self.SaveButton = QPushButton("Enregistrer")
        self.SaveButton.clicked.connect(self.SaveButtonPush)

        if self.greyscale:
            self.pixmap = QPixmap(
                self.resize_image(600, 200, 'Input/grey.jpg', 'Input/grey.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
            self.ChangeColorButton.setHidden(True)
            self.OrdreLine.setHidden(True)

        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0, 1, 4)
        layout.addWidget(self.sous_titre, 1, 0, 1, 4)

        layout.addWidget(self.Image, 0, 5, 4, 4)

        layout.addWidget(QLabel("Epaisseur de la corde:"), 2, 0, 1, 1)
        layout.addWidget(self.EpaisseurLine, 2, 1)
        layout.addWidget(QLabel("Poid de la ligne:"), 3, 0)
        layout.addWidget(self.PoidLine, 3, 1)

        layout.addWidget(QLabel("Ordre des couleurs:"), 4, 0)
        layout.addWidget(self.OrdreLine, 4, 1)

        layout.addWidget(QLabel("Type de resolution:"), 5, 0)
        layout.addWidget(QLabel("Réel:"), 5, 1)
        layout.addWidget(self.checkBox_Real, 5, 2)
        layout.addWidget(QLabel("Recadrer:"), 6, 1)
        layout.addWidget(self.checkBox_Resize, 6, 2)
        layout.addWidget(QLabel("Changer la couleur:"), 7, 0)
        layout.addWidget(self.CouleurChoiceBox, 7, 1)
        layout.addWidget(self.ChangeColorButton, 7, 3)

        layout.addWidget(self.CropButton, 4, 5, 3, 4)

        layout.addWidget(self.DominantImage, 8, 0, 1, 4)
        layout.addWidget(self.SaveButton, 9, 0, 1, 1)

        self.setLayout(layout)

    def checkeReal(self):

        if self.checkBox_Real.checkState():
            self.size = "Real"
            self.checkBox_Resize.setChecked(False)
            print("Real")
        # else:
        #     if self.checkBox_Resize.isCheck():
        #         self.checkBox_Real.setChecked(False)
        #     else:
        #         self.checkBox_Real.setChecked(True)

    def checkeResize(self):

        if self.checkBox_Resize.checkState():
            self.size = "Resize"
            self.checkBox_Real.setChecked(False)
            print("Resize")
        # else:
        #     if self.checkBox_Real.checkState() == False:
        #         self.checkBox_Resize.setChecked(True)
        #     else:
        #         self.checkBox_Resize.setChecked(False)

    def isCouleurChoiceBoxChange(self):
        self.numero_de_couleur = self.CouleurChoiceBox.value()
        return

    def isChangeColorButtonPush(self):

        self.isCouleurChoiceBoxChange()
        color = QColorDialog.getColor()
        # self.temp = self.Realrgb.copy()

        if color.isValid():
            NewRGB = color.getRgb()
            NewRGB = NewRGB[0:3]

            # Pas le choix de faire ça sinon fonctionne pas
            indice = self.numero_de_couleur - 1
            indice = int(indice)

            self.temp[indice] = NewRGB
            self.redoBand(self.temp)

            self.pixmap = QPixmap(self.resize_image(600, 200,
                                                    'Input/bar.jpg', 'Input/bar.jpg'))
            self.DominantImage.setPixmap(self.pixmap)

    def SaveButtonPush(self):

        if self.checkBox_Resize.checkState() == False and self.checkBox_Real.checkState() == False:
            QMessageBox.information(self, 'ERREUR', "Il n'y a pas de type de resolution coche (;", QMessageBox.Ok)
            return

        else:
            self.Realrgb = self.temp
            self.valuepoid = int(self.PoidLine.text())
            self.valueepaisseur = int(self.EpaisseurLine.text())
            self.sequence = self.OrdreLine.text()
            self.submitted2.emit(self.Realrgb, self.size, self.valueepaisseur, self.valuepoid, self.sequence)
            self.close()

    def isCropButtonPush(self):

        lol = [self.image_a_imprimer]
        self.window = Crop(lol)
        self.window.show()

    def resize_image(self, largeur, hauteur, image_path, save_as):

        image = Image.open(image_path)
        resized = image.resize((largeur, hauteur))
        resized.save(save_as)

        return save_as

    def redoBand(self, new_rgb):
        font = cv2.FONT_HERSHEY_SIMPLEX
        bars = []
        onessaye = []

        for index, row in enumerate(new_rgb):
            bar, rgb = self.create_bar(200, 200, row)
            bars.append(bar)
            onessaye.append(rgb)

        img_bar = np.hstack(bars)

        for index, row in enumerate(onessaye):
            image = cv2.putText(img_bar, f'{index + 1}', (5 + 200 * index, 200 - 10),
                                font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.imwrite('Input/bar.jpg', img_bar)

        cv2.waitKey(0)

    def create_bar(self, height, width, color):
        bar = np.zeros((height, width, 3), np.uint8)
        red, green, blue = int(color[0]), int(color[1]), int(color[2])
        bar[:] = (blue, green, red)
        return bar, (red, green, blue)