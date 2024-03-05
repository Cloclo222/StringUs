import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QFileDialog, QComboBox, QMessageBox, QSpinBox, QMenu, QMenuBar
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QFont, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from PIL import Image



class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parametres avancés")
        self.setGeometry(50, 50, 1000, 500)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        #Geometrie
        self.setWindowTitle("STRINGUS")
        self.setGeometry(50, 50, 1000, 500)

        self.Titre = QLabel("STRINGUS: L'Art du Robot")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Faites vos selections")
        self.sous_titre.setFont(QFont('Arial', 20))

        self._createMenuBar()

        #Variable Globale Necessaire
        self.fname = ['C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/no.png']
        self.flag_calculate = False
        self.data_nbcouleur = 1

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

        #Load Button
        load_button = QPushButton("Télécharger")
        load_button.clicked.connect(self.load_clique)

        #Dowload Button
        download_button = QPushButton("Exporter")
        download_button.clicked.connect(self.download_clique)

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

        # Advanced Setting
        advenced_setting_butt = QPushButton("Paramètre avancés")
        advenced_setting_butt.clicked.connect(self.advenced_setting)


        #Nombre de couleur
        self.nb_couleur = QSpinBox(minimum=1, maximum=20, value=1)
        self.nb_couleur.valueChanged.connect(self. nb_couleur_fonct)

        #Image_load Stringus
        self.load = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.fname[0]))
        self.load.setPixmap(self.pixmap)

        #Image Couleur Dominante
        self.dominant_image = QLabel()
        self.pixmap = QPixmap(self.resize_image(600, 200, 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/grey.jpg'))
        self.dominant_image.setPixmap(self.pixmap)

        #Oeuvre en attente
        working = QLabel()
        pixmap = QPixmap(self.resize_image(400, 400, 'C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/work.png'))
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

        # layout.addWidget(load_button, 13, 0)
        # layout.addWidget(download_button, 13, 1)




        # Set the layout on the application's window
        self.setLayout(layout)
        #print(self.children())


    def browse_clique(self):
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
        data_couleur1 = self.Couleur1.currentText()
        data_couleur2 = self.Couleur2.currentText()
        data_couleur3 = self.Couleur3.currentText()
        data_couleur4 = self.Couleur4.currentText()

        if not data_clous or not data_dim or self.fname[0] == 'C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/no.png' :
            QMessageBox.information(self, 'ERREUR', "Information manquante", QMessageBox.Ok)
            self.flag_calculate = False

        else:
            self.flag_calculate = True
            print("Le nombre de clous est de:", data_clous)
            print("Le diametre est de:", data_dim)
            print("La couleur 1 est:", data_couleur1)
            print("La couleur 1 est:", data_couleur2)
            print("La couleur 1 est:", data_couleur3)
            print("La couleur 1 est:", data_couleur4)

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

        number_clusters = self.data_nbcouleur
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
        # print(centers)

        font = cv2.FONT_HERSHEY_SIMPLEX
        bars = []
        rgb_values = []

        for index, row in enumerate(centers):
            bar, rgb = self.create_bar(200, 200, row)
            bars.append(bar)
            rgb_values.append(rgb)

        img_bar = np.hstack(bars)

        for index, row in enumerate(rgb_values):
            image = cv2.putText(img_bar, f'{index + 1}. RGB: {row}', (5 + 200 * index, 200 - 10),
                                font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            print(f'{index + 1}. RGB{row}')

        #cv2.imshow('Image', img)
        #cv2.imshow('Dominant colors', img_bar)

        #filename_dominant = 'C:/Users/Xavier Lefebvre/Documents/GitHub/StringUs/[4] - GUI/bar.jpg'
        #cv2.imwrite(filename_dominant)
        cv2.imwrite('bar.jpg', img_bar)

        cv2.waitKey(0)

        #return filename_dominant


    def nb_couleur_fonct(self):
        self.data_nbcouleur = self.nb_couleur.value()

    def advenced_setting(self):
        w = AnotherWindow()
        w.show()

    def download_clique(self):
        print("Downloading...")

    def load_clique(self):
        print("Loading")

    def _createMenuBar(self):

        menuBar = QMenuBar(self)
        #self.setMenuBar(menuBar)
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



