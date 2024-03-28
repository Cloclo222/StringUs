import sys
import cv2
import csv
import numpy as np
from PIL import Image
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc

import matplotlib
matplotlib.use("TkAgg")

from stringus_code_IDE.COM_python_arduino_UART.SerialArduinoCom.SCARA_COM import *

from .Crop_window1 import *
from ImageProcessing.Canvas import *
from .PA_Window import *
from .Progress_Window import *
from .GetName_Window import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Geometrie de la page
        self.setWindowTitle("STRINGUS")
        self.setGeometry(50, 50, 1000, 500)

        self.Titre = QLabel("STRINGUS: Du virtuel au réel")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Faites vos selections")
        self.sous_titre.setFont(QFont('Arial', 20))

        # Creation du Menu
        self._createActions()
        self._createMenuBar()
        self._connectActions()

        # Variable Globale Necessaire
        self.fnameImage = 'Input/no.png'
        self.data_nbcouleur = 1
        self.rgb_values = []

        # Flags
        self.flag_calculate = False
        self.flag_browse = False
        self.flag_send = False

        # Parametre defaut
        self.GreyScale = False
        self.defautpoid = 10
        self.defautep = 10
        self.sequencedefaut = ""
        self.sequence()
        self.sizedef = "Real"
        self.nbclous = 150
        self.diam = 500
        self.compteur = 0

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

        # Browse document
        BrowseButton = QPushButton("Browse")
        BrowseButton.clicked.connect(self.isBrowseButtonClick)
        self.image_path = QLabel("Vide")
        self.image_path.setMaximumWidth(299)

        # Calculate Button
        CalculateButton = QPushButton("Calculer")
        CalculateButton.clicked.connect(self.isCalculateButtonClick)

        # Envoie Button
        SendButton = QPushButton("Envoyer")
        SendButton.clicked.connect(self.isSendButtonClick)

        # Precedant Button
        PrecedantButton = QPushButton("Precedant")
        PrecedantButton.clicked.connect(self.isPrecedantButtonClick)

        # Suivant Button
        NextButton = QPushButton("Suivant")
        NextButton.clicked.connect(self.isNextButtonClick)

        # Advanced Setting
        PAButton = QPushButton("Paramètre avancés")
        PAButton.clicked.connect(self.isPAButtonClick)

        # Nombre de couleur
        self.NbCouleurBox = QSpinBox(minimum=1, maximum=20, value=1)
        self.NbCouleurBox.valueChanged.connect(self.isNbCouleurChange)

        # Image a imprimer Stringus
        self.VOImage = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, 'Input/no.png'))
        self.VOImage.setPixmap(self.pixmap)

        # Image Couleur Dominante
        self.DominantImage = QLabel()
        self.pixmap = QPixmap(
            self.resize_image(600, 300, 'Input/grey.jpg', 'Input/grey.jpg'))
        self.DominantImage.setPixmap(self.pixmap)

        # Preview de l'oeuvre
        self.PreviewImage = QLabel()
        pixmap = QPixmap(
            self.resize_image(400, 400, 'Input/work.png', 'Input/work.png'))
        self.PreviewImage.setPixmap(pixmap)

        # Check Box grey
        self.GreyBox = QCheckBox()
        self.GreyBox.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.GreyBox.stateChanged.connect(self.GreyBoxCheck)

        # Affichage
        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0, 1, 4)
        layout.addWidget(self.sous_titre, 1, 0, 1, 3)
        layout.addWidget(QLabel("Nombre de clous:"), 2, 0, 1, 2)
        layout.addWidget(self.ClousLine, 2, 2, 1, 2)
        layout.addWidget(self.DimLine, 3, 2, 1, 2)
        layout.addWidget(QLabel("Diametre (mm):"), 3, 0, 1, 2)
        layout.addWidget(BrowseButton, 4, 0, 1, 2)

        layout.addWidget(self.image_path, 4, 2, 1, 2)

        layout.addWidget(QLabel("Nombre de couleur:"), 5, 0)
        layout.addWidget(self.NbCouleurBox, 5, 1)
        layout.addWidget(QLabel("Gris"), 6, 2)
        layout.addWidget(self.GreyBox, 6, 3)

        layout.addWidget(QLabel("Couleurs proposées:"), 6, 0, 1, 2)

        layout.addWidget(self.VOImage, 0, 4, 7, 5)
        layout.addWidget(self.DominantImage, 7, 0, 4, 4)

        layout.addWidget(PAButton, 11, 0, 1, 4)

        layout.addWidget(CalculateButton, 12, 0, 1, 2)
        layout.addWidget(SendButton, 12, 2, 1, 2)
        layout.addWidget(self.PreviewImage, 7, 4, 7, 5)
        layout.addWidget(PrecedantButton, 14, 4, 1, 2)
        layout.addWidget(NextButton, 14, 7, 1, 2)

        # Set the layout on the application's window
        self.setLayout(layout)

    def isBrowseButtonClick(self):

        self.flag_browse = True
        self.flag_calculate = False

        transit = QFileDialog.getOpenFileName(self, 'Open file')
        self.fnameImage = transit[0]
        #
        # if not self.fnameImage:
        #     return
        self.image_path.setText(self.fnameImage)

        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage,"Output/resize_image.png" ))
        self.VOImage.setPixmap(self.pixmap)

        self.analyse_image(self.fnameImage)

        if self.GreyScale:
            self.pixmap = QPixmap(
                self.resize_image(600, 300, 'Input/grey.jpg','Input/grey.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.resize_image(600, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
        self.flag_browse = False

    def isCalculateButtonClick(self):

        self.nbclous = int(self.ClousLine.text())
        data_dim = int(self.DimLine.text())

        if not self.nbclous or not data_dim or self.fnameImage[0] == 'Input/no.png':
            QMessageBox.information(self, 'ERREUR', "Information manquante", QMessageBox.Ok)
            self.flag_calculate = False

        else:
            self.flag_calculate = True

            # self.nameFile = None
            # self.window2 = Window_GetName()
            # self.window2.submitted.connect(self.NameClousCSV)
            # self.window2.setAttribute(Qt.WA_DeleteOnClose)
            # self.window2.show()
            #
            # loop = qtc.QEventLoop()
            # self.window2.destroyed.connect(loop.quit)
            # loop.exec()  # wait ...

            print("Le nombre de clous est de:", self.nbclous)
            print("Le diametre est de:", data_dim)

            Radius = int(self.diam * 2)
            if self.GreyScale is False:

                palette = {}
                keys = range(self.data_nbcouleur)
                values = self.rgb_values
                for i in keys:
                    palette["c%i" % (i + 1)] = values[i]

                args = dict(
                    filename=self.fnameImage,
                    palette=palette,
                    group_orders=self.sequencedefaut,
                    img_radius=Radius,
                    numPins=self.nbclous,
                    lineWidth=self.defautep,
                    lineWeight=self.defautpoid
                )
                canvas = Canvas(**args)
                canvas.buildCanvas()
                output = canvas.paintCanvas()
                output.save('Output/c0.png')
                WriteThreadedCsvFile("Output/ThreadedCSVFile.csv", canvas.totalLines)
                for keys in canvas.img_couleur_sep.keys():
                    im = Image.fromarray(np.uint8(canvas.img_couleur_sep[keys]))
                    im.save("Output/%s.png" % keys)

            else:
                args = dict(
                    filename=self.fnameImage,
                    img_radius=Radius,
                    numPins=self.nbclous,
                    lineWidth=self.defautep,
                    lineWeight=self.defautpoid
                )
                canvas = Canvas(**args)
                canvas.buildCanvas()
                output = canvas.paintCanvas()
                output.save('Output/c0.png')
                WriteThreadedCsvFile("Output/ThreadedCSVFile.csv", canvas.totalLines)
                for keys in canvas.img_couleur_sep.keys():
                    im = Image.fromarray(np.uint8(canvas.img_couleur_sep[keys]))
                    im.save("Output/%s.png" % keys)

            pixmap = QPixmap(
                self.resize_image(400, 400, 'Output/c0.png', 'Output/c0.png'))
            self.PreviewImage.setPixmap(pixmap)

    def isSendButtonClick(self):

        if self.flag_calculate:

            self.flag_send = True
            self.saveCSV()
            self.nbclous = int(self.ClousLine.text())
            self.ProgressBar = Window_Progress("Output/ThreadedCSVFile.csv", self.nbclous)
            self.ProgressBar.show()
            self.flag_send = False

        else:
            QMessageBox.information(self, 'ERREUR', "Il faut calculer avant d'envoyer", QMessageBox.Ok)

    def isNextButtonClick(self):

        if self.GreyScale:
            return

        else:
            self.compteur += 1
            if self.compteur <= self.data_nbcouleur:
                name = "c" + str(self.compteur) + ".png"
                filename = "Output/" + name

            if self.compteur > self.data_nbcouleur:
                self.compteur = self.data_nbcouleur
                name = "c" + str(self.compteur) + ".png"
                filename = "Output/" + name

            pixmap = QPixmap(
                self.resize_image(400, 400, filename, filename))
            self.PreviewImage.setPixmap(pixmap)

    def isPrecedantButtonClick(self):
        self.compteur -= 1
        if self.compteur >= 0:
            name = "c" + str(self.compteur) + ".png"
            filename = "Output/" + name

        if self.compteur < 0:
            self.compteur = 0
            name = "c" + str(self.compteur) + ".png"
            filename = "Output/" + name

        pixmap = QPixmap(
            self.resize_image(400, 400, filename, filename))
        self.PreviewImage.setPixmap(pixmap)

    def isNbCouleurChange(self):
        self.data_nbcouleur = self.NbCouleurBox.value()
        self.sequence()

        if self.fnameImage != 'Input/no.png':
            self.analyse_image(self.fnameImage)
            self.pixmap = QPixmap(
                self.resize_image(600, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
            self.DominantImage.setPixmap(self.pixmap)

    def isPAButtonClick(self):

        # Call fonction pour les parametres d'entree

        if self.rgb_values == []:
            QMessageBox.information(self, 'ERREUR', "Il n'y a pas d'image (;", QMessageBox.Ok)

        else:

            self.PM = Window_PA(self.data_nbcouleur, self.fnameImage, self.rgb_values, self.defautpoid,
                                self.defautep, self.sequencedefaut, self.sizedef, self.GreyScale)
            self.PM.submitted2.connect(self.UpdateValues)
            self.PM.show()

    def GreyBoxCheck(self):

        if self.GreyBox.checkState():
            self.GreyScale = True
            print("here")
            self.pixmap = QPixmap(
                self.resize_image(600, 300, 'Input/grey.jpg','Input/grey.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
            self.NbCouleurBox.setHidden(True)
        else:
            self.GreyScale = False
            self.NbCouleurBox.setHidden(False)
            if self.fnameImage != 'Input/no.png':
                self.analyse_image(self.fnameImage)
                self.pixmap = QPixmap(
                    self.resize_image(600, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
                self.DominantImage.setPixmap(self.pixmap)

    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.LastRunResume)

        # Open Recent submenu
        self.openRecentMenu = fileMenu.addMenu("Open Recent")
        fileMenu.addAction(self.saveAction)

        fileMenu.addAction(self.LastRunResume)

        # Separator
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

    def _createActions(self):
        # File actions
        self.openAction = QAction(QIcon(":file-open.svg"), "&Open...", self)
        self.saveAction = QAction(QIcon(":file-save.svg"), "&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.LastRunResume = QAction("&Last Run Resume", self)

        # String-based key sequences
        self.openAction.setShortcut("Ctrl+O")
        self.saveAction.setShortcut("Ctrl+S")

        # Edit actions
        self.copyAction = QAction(QIcon(":edit-copy.svg"), "&Copy", self)
        self.pasteAction = QAction(QIcon(":edit-paste.svg"), "&Paste", self)
        self.cutAction = QAction(QIcon(":edit-cut.svg"), "C&ut", self)
        # Standard key sequence
        # self.copyAction.setShortcut(QKeySequence.Copy)
        # self.pasteAction.setShortcut(QKeySequence.Paste)
        # self.cutAction.setShortcut(QKeySequence.Cut)

    def _connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        self.LastRunResume.triggered.connect(self.last_run_resume)

        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)

        # Slots

    def last_run_resume(self):

        self.openFile("Parametre/LastRunResume.csv")
        self.nbclous = int(self.ClousLine.text())

        self.ProgressBar = Window_Progress("Output/ThreadedCSVFile.csv", self.nbclous)
        self.ProgressBar.show()

    def openFile(self):
        valeur = [None] * 10
        i = 0
        fichier = [None]*1000

        if self.flag_send:
            fichier = "Parametre\LastRunResume.csv"

            with open(fichier, newline='') as csvfile:
                fichierCSV = csv.reader(csvfile)

                for row in fichierCSV:
                    valeur[i] = row[1]
                    i += 1

        else:
            fichier = QFileDialog.getOpenFileName(self, 'Open file', "CSV files")

            with open(fichier[0], newline='') as csvfile:
                fichierCSV = csv.reader(csvfile)

                for row in fichierCSV:
                    valeur[i] = row[1]
                    i += 1

        self.fnameImage = valeur[3]
        self.data_nbcouleur = int(valeur[4])
        self.defautpoid = int(valeur[6])
        self.defautep = int(valeur[5])
        self.sequencedefaut = valeur[8]
        self.sizedef = valeur[8]
        self.nbclous = int(valeur[1])
        self.diam = int(valeur[2])

        self.image_path.setText(self.fnameImage)

        _, extension = os.path.splitext(self.fnameImage)

        # Vérifier l'extension
        file_to_save = []

        if extension.lower() == '.jpg':
            file_to_save = 'Output/parametre.jpg'
        elif extension.lower() == '.png':
            file_to_save = 'Output/parametre.png'

        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, file_to_save))
        self.VOImage.setPixmap(self.pixmap)
        self.DimLine.setText(valeur[2])
        self.ClousLine.setText(valeur[1])

        self.analyse_image(self.fnameImage)
        self.pixmap = QPixmap(
            self.resize_image(600, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
        self.DominantImage.setPixmap(self.pixmap)
        self.NbCouleurBox.setValue(self.data_nbcouleur)

    def saveFile(self):
        self.nameFile = None
        self.window = Window_GetName()
        self.window.submitted.connect(self.UpdateName)
        self.window.show()

    def saveCSV(self, name):

        name_fichier = "Parametre/" + name

        with open(name_fichier, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(["Nom_du_Paramètre", "Valeur"])
            writer.writerow(["Nombre_de_clous", self.nbclous])
            writer.writerow(["Diametre_du_fil", self.diam])
            writer.writerow(["Nom_du_fichier", self.fnameImage])
            writer.writerow(["Nombre_de_couleur", self.data_nbcouleur])
            writer.writerow(["Epaisseur", self.defautep])
            writer.writerow(["Poid", self.defautpoid])
            writer.writerow(["Sequence", self.sizedef])
            writer.writerow(["Type_de_format", self.sequencedefaut])

    def copyContent(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def openRecentFile(self, filename):
        # Logic for opening a recent file goes here...
        self.centralWidget.setText(f"<b>{filename}</b> opened")

    def UpdateName(self, name_new):
        nameFile = name_new + '.csv'
        self.saveCSV(nameFile)

    def UpdateValues(self, rgb, size, ep, pd, seq):
        self.rgb_values = rgb
        self.defautpoid = pd
        self.defautep = ep
        self.sequencedefaut = seq
        self.sizedef = size

        if self.GreyScale:
            self.pixmap = QPixmap(
                self.resize_image(600, 300, 'Input/grey.jpg', 'Input/grey.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(
                self.resize_image(600, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
            self.DominantImage.setPixmap(self.pixmap)

    def sequence(self):
        self.sequencedefaut = ""

        if self.GreyScale:
            self.sequencedefaut = "c1 c1 c1 c1"

        else:
            for i in range(self.data_nbcouleur):
                self.sequencedefaut = self.sequencedefaut + "c" + str(i + 1) + " "

            self.sequencedefaut = self.sequencedefaut * 4

    def create_bar(self, height, width, color):
        bar = np.zeros((height, width, 3), np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return bar, (red, green, blue)

    def analyse_image(self, filename):

        img = cv2.imread(filename)
        height, width, _ = np.shape(img)
        # print(height, width)

        data = np.reshape(img, (height * width, 3))
        data = np.float32(data)

        number_clusters = self.data_nbcouleur
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
        # print(centers)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bars = []
        self.rgb_values.clear()

        for index, row in enumerate(centers):
            bar, rgb = self.create_bar(200, 200, row)
            bars.append(bar)
            self.rgb_values.append(rgb)

        img_bar = np.hstack(bars)

        for index, row in enumerate(self.rgb_values):
            image = cv2.putText(img_bar, f'{index + 1}', (5 + 200 * index, 200 - 10),
                                font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            # print(f'{index + 1}. RGB{row}')

        cv2.imwrite('Input/bar.jpg', img_bar)

        cv2.waitKey(0)

    def resize_image(self, largeur, hauteur, image_path, save_as):

        image = Image.open(image_path)
        resized = image.resize((largeur, hauteur))

        # if self.flag_browse:
        #     resized.save("Output/resize_image.png")
        #     image_path = "Output/resize_image.png"
        #
        # else:
        resized.save(save_as)

        return save_as

    def NameClousCSV(self, name_new):
        self.nameFileClousCSV = name_new + '.csv'