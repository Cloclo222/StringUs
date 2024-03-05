import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFormLayout, QGridLayout, QHBoxLayout, QLabel, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QDoubleValidator, QFont, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from PIL import Image


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("STRINGUS")
        self.setGeometry(50, 50, 1000, 500)

        self.Titre = QLabel("STRINGUS: L'Art du Robot")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Faites vos selections")
        self.sous_titre.setFont(QFont('Arial', 20))

        #Variable Globale Necessaire
        self.fname = ['C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/walter.png']
        self.flag_calculate = False

        #Box Nombre de clous
        self.clous = QLineEdit()
        self.clous.setValidator(QIntValidator())
        self.clous.setMaxLength(3)
        self.clous.setAlignment(Qt.AlignLeft)
        self.clous.setFont(QFont("Arial", 20))

        #Box Diametre
        self.dim = QLineEdit()
        self.dim.setValidator(QIntValidator())
        self.dim.setMaxLength(4)
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

        #Couleur

        self.Couleur1 = QComboBox()
        self.Couleur1.addItems(['Bleu', 'Rouge', 'Noir', 'Vert'])

        self.Couleur2 = QComboBox()
        self.Couleur2.addItems(['Bleu', 'Rouge', 'Noir', 'Vert'])

        self.Couleur3 = QComboBox()
        self.Couleur3.addItems(['Bleu', 'Rouge', 'Noir', 'Vert'])

        self.Couleur4 = QComboBox()
        self.Couleur4.addItems(['Bleu', 'Rouge', 'Noir', 'Vert'])

        #Logo Stringus
        logo = QLabel()
        pixmap = QPixmap(self.resize_image(200, 200, 'C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/walter.png'))
        logo.setPixmap(pixmap)

        #Oeuvre en attente
        working = QLabel()
        pixmap = QPixmap(self.resize_image(500, 500, 'C:/temp/StringUS/GUI_PYQT5_STRINGUS/Code/work.png'))
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
        layout.addWidget(logo,0,6,2,1)
        layout.addWidget(QLabel("Couleur 1:"), 5, 0)
        layout.addWidget(self.Couleur1,5,1)
        layout.addWidget(QLabel("Couleur 2:"), 6, 0)
        layout.addWidget(self.Couleur2, 6, 1)
        layout.addWidget(QLabel("Couleur 3:"), 7, 0)
        layout.addWidget(self.Couleur3, 7, 1)
        layout.addWidget(QLabel("Couleur 4:"), 8, 0)
        layout.addWidget(self.Couleur4, 8, 1)
        layout.addWidget(calculate_button, 9, 0)
        layout.addWidget(envoyer_button, 9,1)
        layout.addWidget(working,3,5,7,4 )
        layout.addWidget(precedant_button, 11, 5, 1, 2)
        layout.addWidget(suivant_button,11,7,1,2)



        # Set the layout on the application's window
        self.setLayout(layout)
        #print(self.children())


    def browse_clique(self):
        self.fname = QFileDialog.getOpenFileName(self,'Open file')
        self.image_path.setText(self.fname[0])

    def calcul_de_donner(self):
        data_clous = self.clous.text()
        data_dim = self.dim.text()
        data_couleur1 = self.Couleur1.currentText()
        data_couleur2 = self.Couleur2.currentText()
        data_couleur3 = self.Couleur3.currentText()
        data_couleur4 = self.Couleur4.currentText()

        if not data_clous or not data_dim or not self.fname:
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
