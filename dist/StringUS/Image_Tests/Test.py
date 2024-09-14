import sys
import cv2
import csv

import matplotlib
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PIL import Image
from PyQt5 import QtCore as qtc
import time


class Window_ChangeColor(QWidget):
    #submitted3 = qtc.pyqtSignal(bool)
    def __init__(self, rgb):
        super().__init__()

        self.done = False

        self.setWindowTitle("Changement de couleur")
        self.setGeometry(100, 100, 500, 500)

        self.Titre = QLabel("Changement de couleur")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Nouvelle Couleur:")
        self.sous_titre.setFont(QFont('Arial', 20))

        # Resume Button
        self.DoneButton = QPushButton("Resume")
        self.DoneButton.pressed.connect(self.DoneButtonIsClick)

        self.CreatePicture(rgb)

        self.CouleurImage = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, 'Output/Couleur_a_changer.png'))
        self.CouleurImage.setPixmap(self.pixmap)

        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0, 2, 4)
        layout.addWidget(self.sous_titre, 2, 0, 1, 4)
        layout.addWidget(self.CouleurImage, 3, 0, 4, 4)
        layout.addWidget(self.DoneButton, 7, 0)

        self.setLayout(layout)


    def DoneButtonIsClick(self):
        self.done = True
        #self.submitted3.emit(self.done)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setText("This is a message box")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        #msg.setDetailedText("The details are as follows:")
        msg.setIconPixmap(QPixmap('Output/Couleur_a_changer.png'))
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            print("fuck")

        #self.close()
        #print("lol")

    def resize_image(self, largeur, hauteur, image_path):

        image = Image.open(image_path)
        resized = image.resize((largeur, hauteur))
        resized.save(image_path)

        return image_path

    def CreatePicture(self, rgb):
        image = Image.new("RGB", (500,500), rgb)
        image.save('Output/Couleur_a_changer.png')


if __name__ == "__main__":
    rgb = (50,70,0)
    app = QApplication(sys.argv)
    window = Window_ChangeColor((255,255,0))
    window.show()
    sys.exit(app.exec_())