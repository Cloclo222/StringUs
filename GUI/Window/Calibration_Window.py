# Importation des modules nécessaires
# Importation des modules nécessaires
import time

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (
    Qt
)

from stringus_code_IDE.SCARA_COM import *  # Importation de la classe SCARA_COM depuis un module externe


# Définition d'une classe pour la fenêtre d'affichage de la progression
class Window_Calibration(QMainWindow):
    def __init__(self, port_number):
        super(Window_Calibration, self).__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("Calibration")
        self.setGeometry(100, 50, 1500, 900)

        self.setStyleSheet("""
                   QWidget {
                       background-color: lightgrey;
                       color: green;
                   }
                   QLabel {
                       font-family: stylus;
                       color: green;
                   }
                   QLabel#subtitle {
                       color: green;
                   }
                   QLabel#title {
                       color: green;
                   }
                   QLabel#side_label {
                       background-color: green;
                       color: yellow;
                       font-size: 30px;
                       font-weight: bold;
                       padding: 10px;
                       border-radius: 10px;
                       qproperty-alignment: 'AlignCenter';
                       margin-bottom: 10px;
                   }
                   QGroupBox {
                       border: 4px solid green;
                       border-radius: 15px;
                       margin-top: 20px;
                   }
                   QGroupBox::title {
                       subcontrol-origin: margin;
                       subcontrol-position: top left;
                       padding: 0 3px;
                       font-weight: bold;
                       color: green;
                   }
                   QLineEdit, QSpinBox, QCheckBox {
                       background-color: gold;
                       color: green;
                       font-family: stylus;
                   }
                   QPushButton {
                       background-color: white;
                       color: black;
                       font-family: Stylus;
                       font-weight: bold;
                       font-size: 21px;
                       border-style: outset;
                       border-width: 2px;
                       border-radius: 10px;
                       border-color: black;
                   }
                   QPushButton:hover {
                       background-color: green;
                       color: gold;
                   }
               """)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Title
        self.title = QLabel("STRINGUS: Du virtuel au réel")
        self.title.setObjectName("title")
        self.title.setFont(QtGui.QFont('Arial', 30))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.title)

        # Subtitle
        self.subtitle = QLabel("Calibration")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setFont(QtGui.QFont('Arial', 20))
        self.subtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.subtitle)

        # Line under subtitle
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet("color: gold;")
        self.main_layout.addWidget(self.line)

        self.horizontal_layout = QHBoxLayout()
        self.main_layout.addLayout(self.horizontal_layout)

        # Left side layout
        self.left_layout = QVBoxLayout()

        # Left label
        self.left_label = QLabel("Gauche")
        self.left_label.setObjectName("side_label")
        self.left_layout.addWidget(self.left_label, alignment=QtCore.Qt.AlignCenter)

        self.left_group = self.create_group_box("")
        self.left_group.setFont(QtGui.QFont('Arial', 16))
        self.left_buttons_layout = QVBoxLayout()
        self.left_group.setLayout(self.left_buttons_layout)

        self.left_buttons = []
        #Left Button

        self.LeftPositionSeePositionButton = QPushButton("Envoyer robot a approche gauche")
        self.LeftPositionSeePositionButton.pressed.connect(self.LeftPositionSeePositionButtonIsPressed)
        self.LeftPositionSeePositionButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_buttons_layout.addWidget(self.LeftPositionSeePositionButton)
        self.left_buttons.append(self.LeftPositionSeePositionButton)

        self.LeftPositionCalibrationButton = QPushButton("Calibrer Approche Gauche")
        self.LeftPositionCalibrationButton.pressed.connect(self.LeftPositionCalibrationButtonIsPressed)
        self.LeftPositionCalibrationButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_buttons_layout.addWidget(self.LeftPositionCalibrationButton)
        self.left_buttons.append(self.LeftPositionCalibrationButton)

        self.LeftPositionCalibrationRoundButton = QPushButton("Calibrer Cercle Gauche")
        self.LeftPositionCalibrationRoundButton.pressed.connect(self.LeftPositionCalibrationRoundButtonIsPressed)
        self.LeftPositionCalibrationRoundButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_buttons_layout.addWidget(self.LeftPositionCalibrationRoundButton)
        self.left_buttons.append(self.LeftPositionCalibrationRoundButton)

        self.LeftPositionSeeRoundButton = QPushButton("Voir Séquence Complète")
        self.LeftPositionSeeRoundButton.pressed.connect(self.LeftPositionSeeRoundButtonIsPressed)
        self.LeftPositionSeeRoundButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_buttons_layout.addWidget(self.LeftPositionSeeRoundButton)
        self.left_buttons.append(self.LeftPositionSeeRoundButton)

        self.TorqueCheckBox = QCheckBox("Torque moteur active")
        self.TorqueCheckBox.setCheckState(Qt.Checked)

        self.left_buttons_layout.addWidget(self.TorqueCheckBox)
        # For tristate: widget.setCheckState(Qt.PartiallyChecked)
        # Or: widget.setTriState(True)
        self.TorqueCheckBox.clicked.connect(self.TorqueCheckBoxClicked)

        self.left_layout.addWidget(self.left_group)
        self.horizontal_layout.addLayout(self.left_layout)

        # Image Display Section (No Group Box)
        self.image_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.pixmap = QtGui.QPixmap('Input/table.png')
        self.image_label.setPixmap(self.pixmap)
        self.image_layout.addWidget(self.image_label)

        self.horizontal_layout.addLayout(self.image_layout)

        # Right side layout
        self.right_layout = QVBoxLayout()

        # Right label
        self.right_label = QLabel("Droite")
        self.right_label.setObjectName("side_label")
        self.right_layout.addWidget(self.right_label, alignment=QtCore.Qt.AlignCenter)

        self.right_group = self.create_group_box("")
        self.right_group.setFont(QtGui.QFont('Arial', 16))
        self.right_buttons_layout = QVBoxLayout()
        self.right_group.setLayout(self.right_buttons_layout)

        self.right_buttons = []

        self.RightPositionSeePositionButton = QPushButton("Envoyer robot a approche droite")
        self.RightPositionSeePositionButton.pressed.connect(self.RightPositionSeePositionButtonIsPressed)
        self.RightPositionSeePositionButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_buttons_layout.addWidget(self.RightPositionSeePositionButton)
        self.right_buttons.append(self.RightPositionSeePositionButton)

        self.RightPositionCalibrationButton = QPushButton("Calibrer Approche Droite")
        self.RightPositionCalibrationButton.pressed.connect(self.RightPositionCalibrationButtonIsPressed)
        self.RightPositionCalibrationButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_buttons_layout.addWidget(self.RightPositionCalibrationButton)
        self.right_buttons.append(self.RightPositionCalibrationButton)

        self.RightPositionCalibrationRoundButton = QPushButton("Calibrer Cercle Droite")
        self.RightPositionCalibrationRoundButton.pressed.connect(self.RightPositionCalibrationRoundButtonIsPressed)
        self.RightPositionCalibrationRoundButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_buttons_layout.addWidget(self.RightPositionCalibrationRoundButton)
        self.right_buttons.append(self.RightPositionCalibrationRoundButton)

        self.RightPositionSeeRoundButton = QPushButton("Voir Séquence Complète")
        self.RightPositionSeeRoundButton.pressed.connect(self.RightPositionSeeRoundButtonIsPressed)
        self.RightPositionSeeRoundButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_buttons_layout.addWidget(self.RightPositionSeeRoundButton)
        self.right_buttons.append(self.RightPositionSeeRoundButton)

        self.right_layout.addWidget(self.right_group)
        self.horizontal_layout.addLayout(self.right_layout)

        self.scara_com = SCARA_COM(port_number)

        #self.ShowState()

    #def __del__(self):
    # Cleanup code here
    #print("Widget destroyed")
    def closeEvent(self, event):
        print("Widget is closing")
        self.scara_com.arduino.close()
        super().closeEvent(event)

    def create_group_box(self, title):
        group_box = QGroupBox(title)
        return group_box

    def TorqueCheckBoxClicked(self):
        self.scara_com.envoie_commande('{T2}')
        self.ShowState()

    def ShowState(self):
        state = self.scara_com.check_torque()
        print(f"state :  {state}")
        self.TorqueCheckBox.setChecked(state)
        if state:
            self.TorqueCheckBox.setText("Torque moteur active")
        else:
            self.TorqueCheckBox.setText("Torque moteur désactive")
        #QApplication.processEvents()


    # Méthode pour mettre à jour la progression
    def LeftPositionCalibrationButtonIsPressed(self):
        #print("LeftPositionCalibrationButtonIsPressed")
        self.scara_com.envoie_commande('{W0}')
        self.ShowState()

    def LeftPositionSeePositionButtonIsPressed(self):
        #print("LeftPositionSeePositionButtonIsPressed")
        self.scara_com.envoie_commande('{T1}')
        self.scara_com.envoie_commande('{W4}')
        self.ShowState()

    def LeftPositionCalibrationRoundButtonIsPressed(self):
        #print("LeftPositionCalibrationRoundButtonIsPressed")
        self.scara_com.envoie_commande('{T1}')
        self.scara_com.envoie_commande('{W4}')
        self.scara_com.envoie_commande('{T0}')
        self.ShowState()
        self.scara_com.envoie_commande('{W2}')
        self.ShowState()

    def LeftPositionSeeRoundButtonIsPressed(self):
        #print('LeftPositionSeeRoundButtonIsPressed')
        self.scara_com.envoie_commande('{W6}')
        self.ShowState()

    def RightPositionCalibrationButtonIsPressed(self):
        #print('RightPositionCalibrationButtonIsPressed')
        self.scara_com.envoie_commande('{W1}')
        self.ShowState()

    def RightPositionSeePositionButtonIsPressed(self):
        #print('RightPositionSeePositionButtonIsPressed')
        self.scara_com.envoie_commande('{T1}')
        self.scara_com.envoie_commande('{W5}')
        self.ShowState()

    def RightPositionCalibrationRoundButtonIsPressed(self):
        #print('RightPositionCalibrationRoundButtonIsPressed')
        self.scara_com.envoie_commande('{T1}')
        self.scara_com.envoie_commande('{W5}')
        self.scara_com.envoie_commande('{T0}')
        self.ShowState()
        self.scara_com.envoie_commande('{W3}')
        self.ShowState()

    def RightPositionSeeRoundButtonIsPressed(self):
        #print('RightPositionSeeRoundButtonIsPressed')
        self.scara_com.envoie_commande('{W7}')
        self.ShowState()
