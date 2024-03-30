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

        self.LargeurPhoto = QLabel("Largeur")
        self.LargeurPhoto.setFont(QFont('Arial', 9))

        self.HauteurPhoto = QLabel("Hauteur")
        self.HauteurPhoto.setFont(QFont('Arial', 9))

        # Crop Button
        self.CropButton = QPushButton("Crop l'image")
        self.CropButton.clicked.connect(self.isCropButtonPush)

        # Variable
        self.nb_couleur = number_of_color_set
        self.real = filename
        self.size = sizedef

        self.Realrgb = []
        self.Realrgb = rgb_image

        self.valueepaisseur = ep
        self.valueepaisseur = ep
        self.valuepoid = pd
        self.sequence = seq
        self.greyscale = grey
        self.temp = self.Realrgb.copy()

        self.image_a_imprimer = self.real

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

        self.ResizeButton = QPushButton("Recadrer")
        self.ResizeButton.clicked.connect(self.isResizeButtonPush)

        self.LargeurPhotoLine = QLineEdit()
        self.LargeurPhotoLine.setValidator(QIntValidator())
        self.LargeurPhotoLine.setMaxLength(5)
        self.LargeurPhotoLine.setAlignment(Qt.AlignLeft)
        self.LargeurPhotoLine.setFont(QFont("Arial", 10))

        self.HauteurPhotoLine = QLineEdit()
        self.HauteurPhotoLine.setValidator(QIntValidator())
        self.HauteurPhotoLine.setMaxLength(5)
        self.HauteurPhotoLine.setAlignment(Qt.AlignLeft)
        self.HauteurPhotoLine.setFont(QFont("Arial", 10))

        # Image a imprimer
        if sizedef == "Real":
            self.Image = QLabel()
            self.pixmap = QPixmap(self.resize_image(400, 400, self.image_a_imprimer, 'Output/resize_image.png'))
            self.Image.setPixmap(self.pixmap)

        elif sizedef == "Resize":
            self.Image = QLabel()
            self.pixmap = QPixmap(self.image_a_imprimer)
            self.Image.setPixmap(self.pixmap)

        else:  #TEMPORAIRE
            self.Image = QLabel()
            self.pixmap = QPixmap(self.resize_image(400, 400, self.image_a_imprimer, 'Output/resize_image.png'))
            self.Image.setPixmap(self.pixmap)


        # Check Box RealSize
        self.checkBox_Real = QCheckBox()
        self.checkBox_Real.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Real.stateChanged.connect(self.checkeReal)

        # Check Box Resize
        self.checkBox_Resize = QCheckBox()
        self.checkBox_Resize.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Resize.stateChanged.connect(self.checkeResize)

        self.checkBox_Crop = QCheckBox()
        self.checkBox_Crop.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Crop.stateChanged.connect(self.checkCrop)

        # Selection Couleur
        self.CouleurChoiceBox = QSpinBox(minimum=1, maximum=self.nb_couleur, value=1)
        self.CouleurChoiceBox.valueChanged.connect(self.isCouleurChoiceBoxChange)

        # Couleur Dominant_image
        self.DominantImage = QLabel()
        self.pixmap = QPixmap(
            self.resize_image(700, 200, 'Input/bar.jpg', 'Input/bar.jpg'))
        self.DominantImage.setPixmap(self.pixmap)



        # Box ordre
        self.OrdreLine = QLineEdit(seq)
        # self.ordre.setMaxLength(1000)
        self.OrdreLine.setAlignment(Qt.AlignLeft)
        self.OrdreLine.setFont(QFont("Arial", 10))

        # Changement de couleur bouton
        self.ChangeColorButton = QPushButton("Changer la couleur")
        self.ChangeColorButton.clicked.connect(self.isChangeColorButtonPush)





        # Enregistrer Button
        self.SaveButton = QPushButton("Enregistrer")
        self.SaveButton.clicked.connect(self.SaveButtonPush)

        if self.greyscale:
            self.pixmap = QPixmap(
                self.resize_image(700, 200, 'Input/grey.jpg', 'Input/grey.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
            self.ChangeColorButton.setHidden(True)
            self.OrdreLine.setHidden(True)

        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0, 1, 4)
        layout.addWidget(self.sous_titre, 1, 0, 1, 4)

        layout.addWidget(self.Image, 0, 5, 4, 4)

        layout.addWidget(QLabel("Epaisseur de la corde:"), 2, 0, 1, 2)
        layout.addWidget(self.EpaisseurLine, 2, 1, 1, 2)
        layout.addWidget(QLabel("Poid de la ligne:"), 3, 0, 1, 2)
        layout.addWidget(self.PoidLine, 3, 1, 1, 2)

        layout.addWidget(QLabel("Ordre des couleurs:"), 4, 0, 1, 2)
        layout.addWidget(self.OrdreLine, 4, 1, 1, 2)

        layout.addWidget(QLabel("Type de resolution:"), 5, 0)
        layout.addWidget(QLabel("Réel:"), 5, 1)
        layout.addWidget(self.checkBox_Real, 5, 2)

        layout.addWidget(self.LargeurPhoto, 6, 6)
        layout.addWidget(self.HauteurPhoto, 6, 7)

        layout.addWidget(self.LargeurPhotoLine, 7, 6)
        layout.addWidget(self.HauteurPhotoLine, 7, 7)
        layout.addWidget(self.ResizeButton, 8, 6)

        layout.addWidget(QLabel("Recadrer:"), 6, 1)
        layout.addWidget(self.checkBox_Resize, 6, 2)
        layout.addWidget(QLabel("Crop:"), 7, 1)
        layout.addWidget(self.checkBox_Crop, 7, 2)

        layout.addWidget(QLabel("Changer la couleur:"), 8, 0)
        layout.addWidget(self.CouleurChoiceBox, 8, 1)
        layout.addWidget(self.ChangeColorButton, 8, 3, 1, 2)

        layout.addWidget(self.CropButton, 4, 5, 3, 4)

        layout.addWidget(self.DominantImage, 9, 0, 1, 4)
        layout.addWidget(self.SaveButton, 10, 0, 1, 1)

        # self.LargeurPhotoLine.setHidden(True)
        # self.HauteurPhotoLine.setHidden(True)
        # self.LargeurPhoto.setHidden(True)
        # self.HauteurPhoto.setHidden(True)
        # self.ResizeButton.setHidden(True)

        if self.size == "Real":
            self.checkBox_Resize.setChecked(False)
            self.checkBox_Crop.setChecked(False)
            self.checkBox_Real.setChecked(True)

        elif self.size == "Resize":
            self.checkBox_Resize.setChecked(True)
            self.checkBox_Real.setChecked(False)
            self.checkBox_Crop.setChecked(False)

            self.LargeurPhotoLine.setHidden(False)
            self.HauteurPhotoLine.setHidden(False)
            self.LargeurPhoto.setHidden(False)
            self.HauteurPhoto.setHidden(False)
            self.ResizeButton.setHidden(False)

        else:
            self.checkBox_Resize.setChecked(False)
            self.checkBox_Real.setChecked(False)
            self.checkBox_Crop.setChecked(True)
            self.CropButton.setHidden(False)

        self.setLayout(layout)

    def checkCrop(self):

        if self.checkBox_Crop.checkState():
            self.size = "Crop"
            self.checkBox_Resize.setChecked(False)
            self.checkBox_Real.setChecked(False)

            self.LargeurPhotoLine.setHidden(True)
            self.HauteurPhotoLine.setHidden(True)
            self.LargeurPhoto.setHidden(True)
            self.HauteurPhoto.setHidden(True)
            self.ResizeButton.setHidden(True)

            self.CropButton.setHidden(False)

            print("Crop")

    def checkeReal(self):

        if self.checkBox_Real.checkState():

            self.size = "Real"
            self.checkBox_Resize.setChecked(False)
            self.checkBox_Crop.setChecked(False)

            self.LargeurPhotoLine.setHidden(True)
            self.HauteurPhotoLine.setHidden(True)
            self.LargeurPhoto.setHidden(True)
            self.HauteurPhoto.setHidden(True)
            self.ResizeButton.setHidden(True)

            self.CropButton.setHidden(True)

            self.image_a_imprimer = self.real
            self.pixmap = QPixmap(self.resize_image(400, 400, self.image_a_imprimer, 'Output/resize_image.png'))
            self.Image.setPixmap(self.pixmap)

            print("Real")

    def checkeResize(self):

        if self.checkBox_Resize.checkState():
            self.size = "Resize"
            self.checkBox_Real.setChecked(False)
            self.checkBox_Crop.setChecked(False)

            self.LargeurPhotoLine.setHidden(False)
            self.HauteurPhotoLine.setHidden(False)
            self.LargeurPhoto.setHidden(False)
            self.HauteurPhoto.setHidden(False)
            self.CropButton.setHidden(True)
            self.ResizeButton.setHidden(False)

            print("Resize")

    def isCouleurChoiceBoxChange(self):
        self.numero_de_couleur = self.CouleurChoiceBox.value()
        return

    def isResizeButtonPush(self):

        largeur = int(self.LargeurPhotoLine.text())
        hauteur = int(self.HauteurPhotoLine.text())

        self.image_a_imprimer = self.resize_image(largeur, hauteur, self.image_a_imprimer, 'Output/BoxResize.png')
        self.pixmap = QPixmap(self.image_a_imprimer)
        self.Image.setPixmap(self.pixmap)

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

            self.pixmap = QPixmap(self.resize_image(700, 200,
                                                    'Input/bar.jpg', 'Input/bar.jpg'))
            self.DominantImage.setPixmap(self.pixmap)

    def SaveButtonPush(self):

        if self.checkBox_Resize.checkState() == False and self.checkBox_Real.checkState() == False and self.checkBox_Crop.checkState() == False:
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

        lol = ['Output/resize_image.png']
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
