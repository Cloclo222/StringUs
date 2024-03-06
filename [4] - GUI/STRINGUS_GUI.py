import sys
import cv2
import csv
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QFileDialog, QComboBox, QMessageBox, QSpinBox, QMenu, QMenuBar,QAction, QMainWindow, QInputDialog, QVBoxLayout, QCheckBox, QColorDialog

from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QFont, QPixmap, QIcon, QKeySequence
from PyQt5.QtCore import pyqtSlot, Qt
from PIL import Image
from PyQt5 import QtCore as qtc


class Window_PA(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self ,number_of_color:int, filename, flag_bar, rgb_image, data_image):
        super().__init__()
        #Geometrie
        self.setWindowTitle("Parametres avancés")
        #self.setGeometry(50, 50, 1000, 500)

        self.Titre = QLabel("STRINGUS: L'Art du Robot")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Parametres avances")
        self.sous_titre.setFont(QFont('Arial', 20))

        #Variable
        self.nb_couleur = number_of_color
        self.image_a_imprimer = filename
        self.rgb = []
        self.rgb = rgb_image
        self.data = data_image


        #Box Epaisseur de la ligne
        self.epaisseur = QLineEdit()
        self.epaisseur.setValidator(QIntValidator())
        self.epaisseur.setMaxLength(4)
        self.epaisseur.setAlignment(Qt.AlignLeft)
        self.epaisseur.setFont(QFont("Arial", 10))

        # Box Poid de la ligne
        self.poid = QLineEdit()
        self.poid.setValidator(QIntValidator())
        self.poid.setMaxLength(4)
        self.poid.setAlignment(Qt.AlignLeft)
        self.poid.setFont(QFont("Arial", 10))

        #Check Box RealSize
        self.checkBox_Real = QCheckBox()
        self.checkBox_Real.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Real.stateChanged.connect(self.checkeReal)

        #Check Box Resize
        self.checkBox_Resize = QCheckBox()
        self.checkBox_Resize.setGeometry(qtc.QRect(170, 120, 81, 20))
        self.checkBox_Resize.stateChanged.connect(self.checkeResize)

        #Selection Couleur
        self.couleur = QSpinBox(minimum=1, maximum= self.nb_couleur, value=1)
        self.couleur.valueChanged.connect(self.nb_couleur_fonct)


        #Couleur Dominant_image
        self.dominant_image = QLabel()
        if flag_bar:
            self.pixmap = QPixmap(
                self.resize_image(600, 200, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/bar.jpg'))
        else:
            self.pixmap = QPixmap(self.resize_image(600, 200, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/grey.jpg'))
        self.dominant_image.setPixmap(self.pixmap)

        #Image a imprimer
        self.load = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.image_a_imprimer))
        self.load.setPixmap(self.pixmap)

        #Box ordre
        self.ordre = QLineEdit()
        self.ordre.setMaxLength(40)
        self.ordre.setAlignment(Qt.AlignLeft)
        self.ordre.setFont(QFont("Arial", 10))

        #Changement de couleur bouton
        self.changeColor = QPushButton("Changer la couleur")
        self.changeColor.clicked.connect(self.changement_de_couleur)

        #Enregistrer Button
        self.enregistrer_button = QPushButton("Enregistrer")
        self.enregistrer_button.clicked.connect(self.enregistrer)


        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0, 1, 4)
        layout.addWidget(self.sous_titre, 1, 0,1,4)

        layout.addWidget(self.load,0,5,4,4)

        layout.addWidget(QLabel("Epaisseur de la corde:"), 2, 0,1,1)
        layout.addWidget(self.epaisseur, 2, 1)
        layout.addWidget(QLabel("Poid de la ligne:"), 3, 0)
        layout.addWidget(self.poid, 3, 1)

        layout.addWidget(QLabel("Ordre des couleurs:"), 4, 0)
        layout.addWidget(self.ordre, 4, 1)

        layout.addWidget(QLabel("Type de resolution:"), 5, 0)
        layout.addWidget(QLabel("Reel:"), 5,1 )
        layout.addWidget(self.checkBox_Real, 5, 2)
        layout.addWidget(QLabel("Recadrer:"),6, 1)
        layout.addWidget(self.checkBox_Resize, 6, 2)
        layout.addWidget(QLabel("Changer la couleur:"), 7, 0)
        layout.addWidget(self.couleur , 7, 1)
        layout.addWidget(self.changeColor, 7, 3)

        layout.addWidget(self.dominant_image,8,0,1,4)
        layout.addWidget(self.enregistrer_button, 9, 0, 1, 1)


        self.setLayout(layout)

    def checkeReal(self):

        return

    def checkeResize(self):
        return

    def nb_couleur_fonct(self):
        self.numero_de_couleur = self.couleur.value()
        return

    def resize_image(self, largeur, hauteur, image_path):

        image = Image.open(image_path)
        resized = image.resize((largeur, hauteur))
        resized.save(image_path)

        return image_path

    def changement_de_couleur(self):

        self.nb_couleur_fonct()
        color = QColorDialog.getColor()

        if color.isValid():
            lol = color.getRgb()
            self.rgb[self.numero_de_couleur - 1] = lol[0:3]
            self.redoBand(self.rgb)
            self.pixmap = QPixmap(self.resize_image(600, 200,
                                                        'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/bar.jpg'))
            self.dominant_image.setPixmap(self.pixmap)

    def enregistrer(self):
        self.close()

    def redoBand(self, new_rgb):
        number_clusters = self.nb_couleur
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(self.data, number_clusters, None, criteria, 10, flags)
        # print(centers)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bars = []

        for index, row in enumerate(centers):
            bar, rgb = self.create_bar(200, 200, row)
            bars.append(bar)
            new_rgb.append(rgb)

        img_bar = np.hstack(bars)

        for index, row in enumerate(new_rgb):
            image = cv2.putText(img_bar, f'{index + 1}', (5 + 200 * index, 200 - 10),
                                font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.imwrite('bar.jpg', img_bar)

        cv2.waitKey(0)
    def create_bar(self, height, width, color):
        bar = np.zeros((height, width, 3), np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return bar, (red, green, blue)

class Window_GetName(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    submitted = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nom du fichier?")


        self.DataName = None

        self.Ok_button = QPushButton("OK")
        self.Ok_button.clicked.connect(self.Ok_clique)

        self.canc_button = QPushButton("Cancel")
        self.canc_button.clicked.connect(self.canc_clique)

        # Box Name
        self.Name = QLineEdit()
        self.Name.setMaxLength(15)
        self.Name.setAlignment(Qt.AlignLeft)
        self.Name.setFont(QFont("Arial", 10))


        layout = QGridLayout()
        #
        #Add widgets to the layout
        layout.addWidget(QLabel("Nom du fichier:"), 0, 0)
        layout.addWidget(self.Name, 0,1)
        layout.addWidget(self.Ok_button, 1,0)
        layout.addWidget(self.canc_button, 1,1)

        self.setLayout(layout)


    def Ok_clique(self):
        if self.Name.text() == "":
            QMessageBox.information(self, 'ERREUR', "J'ai besoin d'un nom de fichier (;", QMessageBox.Ok)
        else:
            self.submitted.emit(
                self.Name.text()
                )
            self.close()
    def canc_clique(self):
        self.close()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        #Geometrie de la page
        self.setWindowTitle("STRINGUS")
        self.setGeometry(50, 50, 1000, 500)

        self.Titre = QLabel("STRINGUS: L'Art du Robot")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Faites vos selections")
        self.sous_titre.setFont(QFont('Arial', 20))

        #Creation du Menu
        self._createActions()
        self._createMenuBar()
        self._connectActions()

        #Variable Globale Necessaire
        self.fname = ['C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/no.png']
        self.flag_calculate = False
        self.flag_couleur = True
        self.data_nbcouleur = 1
        self.fnameCouleurBar = ""
        self.flag_bar = False
        self.rgb_values = []

        #Box Nombre de clous
        self.clous = QLineEdit()
        self.clous.setValidator(QIntValidator())
        self.clous.setMaxLength(4)
        self.clous.setAlignment(Qt.AlignLeft)
        self.clous.setFont(QFont("Arial", 20))

        #Box Diametre
        self.dim = QLineEdit()
        self.dim.setValidator(QIntValidator())
        self.dim.setMaxLength(3)
        self.dim.setAlignment(Qt.AlignLeft)
        self.dim.setFont(QFont("Arial", 20))

        #Browse document
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_clique)
        self.image_path = QLabel("Vide")

        #Calculate Button
        calculate_button = QPushButton("Calculer")
        calculate_button.clicked.connect(self.calcul_de_donner)

        #Envoie Button
        envoyer_button = QPushButton("Envoyer")
        envoyer_button.clicked.connect(self.envoyer)

        #Precedant Button
        precedant_button = QPushButton("Precedant")
        precedant_button.clicked.connect(self.precedant)

        #Suivant Button
        suivant_button = QPushButton("Suivant")
        suivant_button.clicked.connect(self.suivant)

        #Advanced Setting
        advenced_setting_butt = QPushButton("Paramètre avancés")
        advenced_setting_butt.clicked.connect(self.advenced_setting)

        #Nombre de couleur
        self.nb_couleur = QSpinBox(minimum=1, maximum=20, value=1)
        self.nb_couleur.valueChanged.connect(self. nb_couleur_fonct)

        #Image a imprimer Stringus
        self.load = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.fname[0]))
        self.load.setPixmap(self.pixmap)

        #Image Couleur Dominante
        self.dominant_image = QLabel()
        self.pixmap = QPixmap(self.resize_image(600, 200, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/grey.jpg'))
        self.dominant_image.setPixmap(self.pixmap)

        #Preview de l'oeuvre
        working = QLabel()
        pixmap = QPixmap(self.resize_image(400, 400, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/work.png'))
        working.setPixmap(pixmap)

        #Affichage
        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0,1,4)
        layout.addWidget(self.sous_titre, 1, 0)
        layout.addWidget(QLabel("Nombre de clous:"),2,0)
        layout.addWidget(self.clous,2,1)
        layout.addWidget(self.dim, 3, 1)
        layout.addWidget(QLabel("Diametre (mm):"), 3, 0)
        layout.addWidget(browse_button, 4, 0)
        layout.addWidget(self.image_path, 4, 1)
        layout.addWidget(self.load,0,5,4,4)
        layout.addWidget(QLabel("Nombre de couleur:"), 5, 0)
        layout.addWidget(self.nb_couleur, 5, 1)

        layout.addWidget(QLabel("Couleurs proposées:"), 6, 0)
        layout.addWidget(self.dominant_image, 7, 0,1,2)

        layout.addWidget(advenced_setting_butt, 8, 0, 1, 2)

        layout.addWidget(calculate_button, 10, 0)
        layout.addWidget(envoyer_button, 10,1)
        layout.addWidget(working,5,5,7,4 )
        layout.addWidget(precedant_button, 13, 5, 1, 2)
        layout.addWidget(suivant_button,13,7,1,2)

        # Set the layout on the application's window
        self.setLayout(layout)

    def browse_clique(self):
        self.flag_bar = True
        self.fname = QFileDialog.getOpenFileName(self,'Open file')
        self.image_path.setText(self.fname[0])

        self.pixmap = QPixmap(self.resize_image(400, 400, self.fname[0]))
        self.load.setPixmap(self.pixmap)

        self.analyse_image(self.fname[0])
        self.pixmap = QPixmap(self.resize_image(600, 200, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/bar.jpg'))
        self.dominant_image.setPixmap(self.pixmap)

    def calcul_de_donner(self):
        data_clous = self.clous.text()
        data_dim = self.dim.text()

        if not data_clous or not data_dim or self.fname[0] == 'C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/no.png' :
            QMessageBox.information(self, 'ERREUR', "Information manquante", QMessageBox.Ok)
            self.flag_calculate = False

        else:
            self.flag_calculate = True
            print("Le nombre de clous est de:", data_clous)
            print("Le diametre est de:", data_dim)

    def envoyer(self):
        if self.flag_calculate:
            print("lol")

        else:
            QMessageBox.information(self, 'ERREUR', "Il faut calculer avant d'envoyer", QMessageBox.Ok)

    def resize_image(self, largeur, hauteur, image_path):

        image = Image.open(image_path)
        resized = image.resize((largeur, hauteur))
        resized.save(image_path)

        return image_path

    def suivant(self):
        print("lol")

    def precedant(self):
        print("lol")

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

        self.data_pour_PA = data
        number_clusters = self.data_nbcouleur
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
        # print(centers)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bars = []


        for index, row in enumerate(centers):
            bar, rgb = self.create_bar(200, 200, row)
            bars.append(bar)
            self.rgb_values.append(rgb)

        img_bar = np.hstack(bars)

        for index, row in enumerate(self.rgb_values):
            image = cv2.putText(img_bar, f'{index + 1}', (5 + 200 * index, 200 - 10),
                                font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            #print(f'{index + 1}. RGB{row}')

        cv2.imwrite('bar.jpg', img_bar)

        cv2.waitKey(0)

    def nb_couleur_fonct(self):
        self.data_nbcouleur = self.nb_couleur.value()

        if self.fname[0] != 'C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/no.png' and self.flag_couleur == True:
            self.analyse_image(self.fname[0])
            self.pixmap = QPixmap(self.resize_image(600, 200, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/bar.jpg'))
            self.dominant_image.setPixmap(self.pixmap)

    def advenced_setting(self):

        #Call fonction pour les parametres d'entree

        if self.rgb_values == []:
            QMessageBox.information(self, 'ERREUR', "Il n'y a pas d'image (;", QMessageBox.Ok)

        else:
            self.flag_couleur = False
            self.nb_couleur_fonct()
            self.flag_couleur = True

            self.PM = Window_PA(self.data_nbcouleur, self.fname[0], self.flag_bar, self.rgb_values, self.data_pour_PA)
            self.PM.show()

    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        #self.setMenuBar(menuBar)
        #menuBar = self.menuBar()
        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        # Open Recent submenu
        self.openRecentMenu = fileMenu.addMenu("Open Recent")
        fileMenu.addAction(self.saveAction)
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

        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)

        # Slots
    def openFile(self):
        # Logic for opening an existing file goes here...
        self.centralWidget.setText("<b>File > Open...</b> clicked")

    def saveFile(self):
        self.NewWindow()

    def saveCSV(self, name):

        with open(name, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(["SNo", "Name", "Subject"])
            writer.writerow([1, "Ash Ketchum", "English"])
            writer.writerow([2, "Gary Oak", "Mathematics"])
            writer.writerow([3, "Brock Lesner", "Physics"])

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

    @qtc.pyqtSlot(str)
    def UpdateName(self, name_new):
         nameFile = name_new + '.csv'
         self.saveCSV(nameFile)

    def NewWindow(self):

        self.nameFile = None
        self.window = Window_GetName()
        self.window.submitted.connect(self.UpdateName)
        self.window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



