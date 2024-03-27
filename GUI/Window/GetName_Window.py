from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc



class Window_GetName(QWidget):
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
        # Add widgets to the layout
        layout.addWidget(QLabel("Nom du fichier:"), 0, 0)
        layout.addWidget(self.Name, 0, 1)
        layout.addWidget(self.Ok_button, 1, 0)
        layout.addWidget(self.canc_button, 1, 1)

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