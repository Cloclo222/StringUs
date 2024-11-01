import ast

# matplotlib.use("TkAgg")

from .PA_Window import *
from .Progress_Window import *
from .GetName_Window import *
from .Calibration_Window import *
from .Detection_Window import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Geometrie de la page
        self.setWindowTitle("STRINGUS")
        self.setGeometry(50, 50, 1, 1)

        # self.setStyleSheet("""
        #                    QWidget {
        #                        background-color: lightgrey;
        #                        color: green;
        #                    }
        #                    QLabel {
        #                        font-family: stylus;
        #                        color: Black;
        #                        border-radius: 50px;
        #
        #
        #                    }
        #                    QLabel#subtitle {
        #                        color: green;
        #                    }
        #                    QLabel#title {
        #                        color: green;
        #                    }
        #                    QLabel#side_label {
        #                        background-color: green;
        #                        color: yellow;
        #                        font-size: 30px;
        #                        font-weight: bold;
        #                        padding: 10px;
        #                        border-radius: 10px;
        #                        qproperty-alignment: 'AlignCenter';
        #                        margin-bottom: 10px;
        #                    }
        #                    QGroupBox {
        #                        border: 4px solid green;
        #                        border-radius: 15px;
        #                        margin-top: 20px;
        #                    }
        #                    QGroupBox::title {
        #                        subcontrol-origin: margin;
        #                        subcontrol-position: top left;
        #                        padding: 0 3px;
        #                        font-weight: bold;
        #                        color: green;
        #                    }
        #                    QLineEdit, QSpinBox, QCheckBox {
        #                        background-color: white;
        #                        color: green;
        #                        font-family: stylus;
        #                        border-radius: 10px;
        #                    }
        #                    QPushButton {
        #                        background-color: white;
        #                        color: black;
        #                        font-family: Stylus;
        #                        font-weight: bold;
        #                        font-size: 21px;
        #                        border-style: outset;
        #                        border-width: 2px;
        #                        border-radius: 10px;
        #                        border-color: black;
        #                    }
        #                    QPushButton:hover {
        #                        background-color: green;
        #                        color: gold;
        #                    }
        #                """)

        self.Titre = QLabel("STRINGUS: Du virtuel au réel")
        self.Titre.setObjectName("title")
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
        self.flag_simulation = False
        self.flag_OpenCSV = False
        self.flag_sequenceCalculate = False

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
        self.TotalNumberLines = 0
        self.offset = 0
        self.portArduino = -1

        self.detect_openRB150()

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
        CalculateButton.setMinimumHeight(50)

        # Envoie Button
        SendButton = QPushButton("Envoyer")
        SendButton.clicked.connect(self.isSendButtonClick)
        SendButton.setMinimumHeight(50)

        # Precedant Button
        PrecedantButton = QPushButton("Precedant")
        PrecedantButton.clicked.connect(self.isPrecedantButtonClick)
        PrecedantButton.setMinimumHeight(50)

        self.SimulationButton = QPushButton("Créer la simulation")
        self.SimulationButton.clicked.connect(self.isSimulationButtonClick)
        self.SimulationButton.setMinimumHeight(20)

        # Suivant Button
        NextButton = QPushButton("Suivant")
        NextButton.clicked.connect(self.isNextButtonClick)
        NextButton.setMinimumHeight(50)

        self.RecalculateSequenceButton = QPushButton("Recalculer avec nouvelle séquence")
        self.RecalculateSequenceButton.clicked.connect(self.isRecalculateSequenceButtonClick)
        self.RecalculateSequenceButton.setMinimumHeight(20)

        # Advanced Setting
        PAButton = QPushButton("Paramètre avancés")
        PAButton.clicked.connect(self.isPAButtonClick)

        # Nombre de couleur
        self.NbCouleurBox = QSpinBox(minimum=1, maximum=20, value=1)
        self.NbCouleurBox.valueChanged.connect(self.isNbCouleurChange)
        self.NbCouleurBox.setMinimumHeight(40)
        font = self.NbCouleurBox.font()
        font.setPointSize(12)
        self.NbCouleurBox.setFont(font)

        # Image a imprimer Stringus
        self.VOImage = QLabel()
        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, 'Input/no.png'))
        self.VOImage.setPixmap(self.pixmap)

        # Image Couleur Dominante
        self.DominantImage = QLabel()
        self.pixmap = QPixmap(
            self.resize_image(700, 300, 'Input/grey.jpg', 'Input/grey.jpg'))
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
        # layout.setSpacing(0)
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

        layout.addWidget(self.SimulationButton, 12, 0, 1, 2)

        layout.addWidget(self.RecalculateSequenceButton, 14, 0, 1, 2)

        layout.addWidget(CalculateButton, 15, 0, 1, 2)
        layout.addWidget(SendButton, 15, 2, 1, 2)
        layout.addWidget(self.PreviewImage, 7, 4, 7, 5)
        layout.addWidget(PrecedantButton, 14, 4, 1, 2)
        layout.addWidget(NextButton, 14, 7, 1, 2)

        self.RecalculateSequenceButton.setHidden(True)
        self.SimulationButton.setHidden(True)
        # Set the layout on the application's window
        self.setLayout(layout)

    def isSimulationButtonClick(self):
        self.flag_simulation = True
        self.canvas.animate(fps=60)
        QMessageBox.information(self, 'Simulation',
                                "La simulation est prête et elle se trouve maintenant dans vos dossiers",
                                QMessageBox.Ok)

    def isBrowseButtonClick(self):

        self.flag_browse = True
        self.flag_calculate = False
        self.flag_simulation = False

        self.transit = QFileDialog.getOpenFileName(self, 'Open file')
        self.fnameImage = self.transit[0]
        #
        # if not self.fnameImage:
        #     return
        if self.fnameImage:
            self.image_path.setText(self.fnameImage)
            self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, "Output/resize_image.png"))
            self.VOImage.setPixmap(self.pixmap)

            self.analyse_image(self.fnameImage)

            if self.GreyScale:
                self.pixmap = QPixmap(
                    self.resize_image(700, 300, 'Input/grey.jpg', 'Input/grey.jpg'))
                self.DominantImage.setPixmap(self.pixmap)
            else:
                self.pixmap = QPixmap(
                    self.resize_image(700, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
                self.DominantImage.setPixmap(self.pixmap)
            self.flag_browse = False

            self.RecalculateSequenceButton.setHidden(True)
            self.SimulationButton.setHidden(True)

    def isRecalculateSequenceButtonClick(self):

        self.canvas.group_orders = self.sequencedefaut
        self.canvas.OrderColours()
        output = self.canvas.paintCanvas()
        output.save('Output/c0.png')
        WriteThreadedCsvFile("Output/ThreadedCSVFile.csv", self.canvas.totalLines)

        pixmap = QPixmap(
            self.resize_image(400, 400, 'Output/c0.png', 'Output/c0.png'))
        self.PreviewImage.setPixmap(pixmap)

        self.TotalNumberLines = self.canvas.getNumLines()

    def isCalculateButtonClick(self):

        self.nbclous = int(self.ClousLine.text())
        data_dim = int(self.DimLine.text())

        if not self.nbclous or not data_dim or self.fnameImage[0] == 'Input/no.png':
            QMessageBox.information(self, 'ERREUR', "Information manquante", QMessageBox.Ok)
            self.flag_calculate = False

        else:
            self.flag_calculate = True

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
                self.canvas = Canvas(**args)
                self.canvas.buildCanvas()
                output = self.canvas.paintCanvas()
                output.save('Output/c0.png')
                WriteThreadedCsvFile("Output/ThreadedCSVFile.csv", self.canvas.totalLines)
                for keys in self.canvas.img_couleur_sep.keys():
                    im = Image.fromarray(np.uint8(self.canvas.img_couleur_sep[keys]))
                    im.save("Output/%s.png" % keys)


            else:

                args = dict(
                    filename=self.fnameImage,
                    img_radius=Radius,
                    numPins=self.nbclous,
                    lineWidth=self.defautep,
                    lineWeight=self.defautpoid
                )
                self.canvas = Canvas(**args)
                self.canvas.buildCanvas()
                output = self.canvas.paintCanvas()
                output.save('Output/c0.png')
                WriteThreadedCsvFile("Output/ThreadedCSVFile.csv", self.canvas.totalLines)
                for keys in self.canvas.img_couleur_sep.keys():
                    im = Image.fromarray(np.uint8(self.canvas.img_couleur_sep[keys]))
                    im.save("Output/%s.png" % keys)

            pixmap = QPixmap(
                self.resize_image(400, 400, 'Output/c0.png', 'Output/c0.png'))
            self.PreviewImage.setPixmap(pixmap)

            self.TotalNumberLines = self.canvas.getNumLines()
            self.RecalculateSequenceButton.setHidden(False)
            self.SimulationButton.setHidden(False)

    def isSendButtonClick(self):

        if self.flag_calculate and self.portArduino != -1:

            if not self.flag_simulation:
                self.canvas.generateImgs()

            self.flag_send = True
            self.saveCSV("LastRunResume.csv")
            self.nbclous = int(self.ClousLine.text())
            self.ProgressBar = Window_Progress("Output/ThreadedCSVFile.csv", self.nbclous, self.TotalNumberLines,
                                               self.portArduino)
            self.ProgressBar.show()
            self.flag_send = False

            QMessageBox.information(self, 'ENVOYER',
                                    "Assurer vous d'avoir recalculer si vous avez changé des données depuis le dernier calcul",
                                    QMessageBox.Ok)

        elif self.portArduino == -1:
            QMessageBox.information(self, 'ERREUR', "Il n'y a pas d'Arduino de connecté", QMessageBox.Ok)

        else:
            QMessageBox.information(self, 'ERREUR', "Il faut calculer avant d'envoyer", QMessageBox.Ok)

    def isNextButtonClick(self):

        if self.GreyScale:
            return
        if self.flag_calculate:
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
        else:
            QMessageBox.information(self, 'ERREUR', "Il faut calculer avant", QMessageBox.Ok)

    def isPrecedantButtonClick(self):

        if self.GreyScale:
            return
        if self.flag_calculate:
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
        else:
            QMessageBox.information(self, 'ERREUR', "Il faut calculer avant", QMessageBox.Ok)

    def isNbCouleurChange(self):

        self.RecalculateSequenceButton.setHidden(True)
        self.SimulationButton.setHidden(True)
        self.flag_calculate = False
        if not self.flag_OpenCSV:
            self.data_nbcouleur = self.NbCouleurBox.value()
            self.sequence()

            if self.fnameImage != 'Input/no.png':
                self.analyse_image(self.fnameImage)
                self.pixmap = QPixmap(
                    self.resize_image(700, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
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
            # print("here")
            self.pixmap = QPixmap(
                self.resize_image(700, 300, 'Input/grey.jpg', 'Input/grey.jpg'))
            self.DominantImage.setPixmap(self.pixmap)
            self.NbCouleurBox.setHidden(True)
        else:
            self.GreyScale = False
            self.NbCouleurBox.setHidden(False)
            if self.fnameImage != 'Input/no.png':
                self.analyse_image(self.fnameImage)
                self.pixmap = QPixmap(
                    self.resize_image(700, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
                self.DominantImage.setPixmap(self.pixmap)

    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        # fileMenu.addAction(self.LastRunResume)

        # Open Recent submenu
        self.openRecentMenu = fileMenu.addMenu("Open Recent")
        fileMenu.addAction(self.saveAction)

        fileMenu.addAction(self.LastRunResume)

        # fileMenu.addAction(self.Calibration)

        # Separator
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        # Edit menu
        # editMenu = menuBar.addMenu("&Edit")
        # editMenu.addAction(self.copyAction)
        # editMenu.addAction(self.pasteAction)
        # editMenu.addAction(self.cutAction)

        # Edit menu
        ToolsMenu = menuBar.addMenu("&Tools")
        ToolsMenu.addAction(self.CalibrationAction)
        ToolsMenu.addAction(self.PortAction)

    def _createActions(self):
        # File actions
        self.openAction = QAction(QIcon(":file-open.svg"), "&Open...", self)
        self.saveAction = QAction(QIcon(":file-save.svg"), "&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.LastRunResume = QAction("&Last Run Resume", self)
        # self.Calibration = QAction("&Calibration", self)

        # String-based key sequences
        self.openAction.setShortcut("Ctrl+O")
        self.saveAction.setShortcut("Ctrl+S")
        self.LastRunResume.setShortcut("Ctrl+L")

        # Edit actions
        # self.copyAction = QAction(QIcon(":edit-copy.svg"), "&Copy", self)
        # self.pasteAction = QAction(QIcon(":edit-paste.svg"), "&Paste", self)
        # self.cutAction = QAction(QIcon(":edit-cut.svg"), "C&ut", self)
        # Standard key sequence
        # self.copyAction.setShortcut(QKeySequence.Copy)
        # self.pasteAction.setShortcut(QKeySequence.Paste)
        # self.cutAction.setShortcut(QKeySequence.Cut)

        self.CalibrationAction = QAction("&Calibration", self)
        self.PortAction = QAction("&Connection Port", self)

    def _connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        self.LastRunResume.triggered.connect(self.last_run_resume)

        # Connect Edit actions
        # self.copyAction.triggered.connect(self.copyContent)
        # self.pasteAction.triggered.connect(self.pasteContent)
        # self.cutAction.triggered.connect(self.cutContent)

        # Slots
        self.CalibrationAction.triggered.connect(self.CalibrationIsTriggered)
        self.PortAction.triggered.connect(self.PortIsTriggered)

    def last_run_resume(self):
        self.flag_send = True
        self.openFile()
        self.nbclous = int(self.ClousLine.text())
        self.flag_send = False

        self.detect_openRB150()

        if self.portArduino == -1:
            QMessageBox.information(self, 'ERREUR', "Il n'y a pas d'Arduino de connecté", QMessageBox.Ok)
        else:
            self.ProgressBar = Window_Progress("Output/ThreadedCSVFile.csv", self.nbclous, self.TotalNumberLines,self.portArduino)
            self.ProgressBar.show()

    def CalibrationIsTriggered(self):
        if self.portArduino == -1:
            QMessageBox.information(self, 'ERREUR', "Il n'y a pas d'Arduino de connecté", QMessageBox.Ok)
        else:
            transit = "COM" + str(self.portArduino)
            self.Cal = Window_Calibration(self.portArduino)
            self.Cal.show()

    def PortIsTriggered(self):
        self.PO = Window_Detection(self.portArduino)
        self.PO.submitted3.connect(self.UpdateValuesPort)
        self.PO.show()

    def UpdateValuesPort(self, port):
        self.portArduino = port

    def openFile(self):
        valeur = [None] * 15
        i = 0
        fichier = [None] * 1000

        if self.flag_send:
            fichier = "Parametre/LastRunResume.csv"

            with open(fichier, newline='') as csvfile:
                fichierCSV = csv.reader(csvfile)

                for row in fichierCSV:
                    valeur[i] = row[1]
                    i += 1

        else:
            fichier = QFileDialog.getOpenFileName(self,
                                                  'Open file',
                                                  "Parametre")
            if fichier[0]:
                with open(fichier[0], newline='') as csvfile:
                    fichierCSV = csv.reader(csvfile)

                    for row in fichierCSV:
                        valeur[i] = row[1]
                        i += 1

        self.fnameImage = valeur[3]
        self.data_nbcouleur = int(valeur[4])
        self.defautpoid = int(valeur[6])
        self.defautep = int(valeur[5])
        self.sequencedefaut = valeur[11]
        self.sizedef = valeur[8]
        self.nbclous = int(valeur[1])
        self.diam = int(valeur[2])
        self.TotalNumberLines = int(valeur[9])
        string_rgb = str(valeur[10])
        self.rgb_values = ast.literal_eval(string_rgb)


        self.image_path.setText(self.fnameImage)

        _, extension = os.path.splitext(self.fnameImage)

        # Vérifier l'extension
        file_to_save = []

        if extension.lower() == '.jpg':
            file_to_save = 'Output/parametre.jpg'
        elif extension.lower() == '.png':
            file_to_save = 'Output/parametre.png'
        elif extension.lower() == '.jpeg':
            file_to_save = 'Output/parametre.jpeg'

        self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, file_to_save))
        self.VOImage.setPixmap(self.pixmap)
        self.DimLine.setText(valeur[2])
        self.ClousLine.setText(valeur[1])

        # self.analyse_image(self.fnameImage)
        rgb = []
        for t in self.rgb_values:
            rgb.append(t[::-1])

        self.redoBand(rgb)

        self.pixmap = QPixmap(
            self.resize_image(700, 300, 'Input/bar.jpg', 'Input/bar.jpg'))
        self.DominantImage.setPixmap(self.pixmap)

        self.flag_OpenCSV = True
        self.NbCouleurBox.setValue(self.data_nbcouleur)
        self.flag_OpenCSV = False

    def saveFile(self):
        self.nameFile = None
        self.window = Window_GetName()
        self.window.submitted.connect(self.UpdateName)
        self.window.show()

    def saveCSV(self, name):

        name_fichier = "Parametre/" + name

        self.nbclous = int(self.ClousLine.text())
        self.diam = int(self.DimLine.text())

        with open(name_fichier, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(["Nom_du_Paramètre", "Valeur"])
            writer.writerow(["Nombre_de_clous", self.nbclous])
            writer.writerow(["Diametre_du_fil", self.diam])
            writer.writerow(["Nom_du_fichier", self.fnameImage])
            writer.writerow(["Nombre_de_couleur", self.data_nbcouleur])
            writer.writerow(["Epaisseur", self.defautep])
            writer.writerow(["Poid", self.defautpoid])
            writer.writerow(["Taille_image", self.sizedef])
            writer.writerow(["Type_de_format", self.sequencedefaut])
            writer.writerow(["Nombre_de_ligne_total_canvas", self.TotalNumberLines])
            writer.writerow(["RGB", self.rgb_values])
            writer.writerow(["Sequence", self.sequencedefaut])

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

        if self.sizedef == "Real":
            self.fnameImage = self.transit[0]
            self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, "Output/resize_image.png"))


        elif self.sizedef == "Crop":
            self.pixmap = QPixmap(self.resize_image(400, 400, self.fnameImage, "Output/resize_image.png"))

        elif self.sizedef == "Resize":
            self.fnameImage = 'Output/BoxResize.png'
            self.pixmap = QPixmap('Output/BoxResize.png')

        self.VOImage.setPixmap(self.pixmap)

        if self.GreyScale:
            self.pixmap = QPixmap(
                self.resize_image(700, 300, 'Input/grey.jpg', 'Input/grey.jpg'))

        else:
            self.pixmap = QPixmap(
                self.resize_image(700, 300, 'Input/bar.jpg', 'Input/bar.jpg'))

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

    def detect_openRB150(self):
        """
        Detect if an openRB-150 is connected to the serial ports.
        """
        openRB150_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB Serial Device' in p.description or 'Périphérique série USB' in p.description # Replace with the exact description
        ]

        if not openRB150_ports:
            self.portArduino = -1
            print("No open serial ports")
            return False
        else:
            self.portArduino = self.extract_numbers_and_convert(openRB150_ports[0])
            return f"openRB-150 found on port(s): {', '.join(openRB150_ports)}"

    def extract_numbers_and_convert(self, string):
        # Keep only the digits
        digits = ''.join([char for char in string if char.isdigit()])
        # Convert the string of digits to an integer
        return int(digits)
