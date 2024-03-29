from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc
from stringus_code_IDE.COM_python_arduino_UART.SerialArduinoCom.SCARA_COM import *

from ImageProcessing.Canvas import *


class WorkerSignals(QObject):
    progress = qtc.pyqtSignal(int, bool, tuple, int, int)
    # color = qtc.pyqtSignal(bool)


class JobRunner(QRunnable):
    signals = WorkerSignals()

    # ChangeColor = WorkerSignals()

    def __init__(self, filename, nb_clous, TotalLinesCanvas):
        super().__init__()

        self.TotalLinesCanvas = TotalLinesCanvas
        self.filename = filename
        self.is_paused = False
        self.is_killed = False
        self.scara_com = SCARA_COM(7)  # TODO : CUM
        self.scara_com.readThreadedCSV(filename, nb_clous)
        self.NumCSVLines = self.scara_com.getNumLinesCSV()
        self.need_change = False

    @pyqtSlot()
    def run(self):

        for index, cmd in enumerate(self.scara_com.commandes):

            percent = int(index + (self.TotalLinesCanvas - self.NumCSVLines) / self.TotalLinesCanvas * 100)
            self.signals.progress.emit(percent, self.need_change, self.scara_com.pinColours[index], index,
                                       self.NumCSVLines)

            if index == 0:
                self.need_change = True
                self.is_paused = True
                self.signals.progress.emit(percent, self.need_change, self.scara_com.pinColours[index], index,
                                           self.NumCSVLines)

            self.scara_com.send_one_line(index, cmd)
            self.EraseCSVLine()
            time.sleep(0.1)

            if self.scara_com.pinColours[index] != self.scara_com.pinColours[index - 1] and index > 0:
                self.need_change = True
                self.is_paused = True
                self.signals.progress.emit(percent, self.need_change, self.scara_com.pinColours[index], index,
                                           self.NumCSVLines)

            while self.is_paused:
                time.sleep(0)

            self.need_change = False

            if self.is_killed:
                break

    def CreatePicture(self, rgb):
        image = Image.new("RGB", (100, 100), rgb)
        image.save('Output/Couleur_a_changer.png')

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def kill(self):
        self.is_killed = True

    def EraseCSVLine(self):
        df = pd.read_csv(self.filename)
        df = df.drop(0)
        df.to_csv(self.filename, index=False)


class Window_Progress(QWidget):

    def __init__(self, filename, nb_clous, TotalLinesCanvas):
        super().__init__()

        self.setWindowTitle("Information Robot")
        self.setGeometry(100, 100, 500, 500)

        self.Titre = QLabel("STRINGUS: Du virtuel au réel")
        self.Titre.setFont(QFont('Arial', 30))

        self.sous_titre = QLabel("Information Robot")
        self.sous_titre.setFont(QFont('Arial', 20))

        # Thread runner
        self.threadpool = QThreadPool()

        # Create a runner
        self.runner = JobRunner(filename, nb_clous, TotalLinesCanvas)
        self.runner.signals.progress.connect(self.update_progress)
        self.threadpool.start(self.runner)

        self.Image = QLabel()
        self.pixmap = QPixmap('Output/Couleur_a_changer.png')
        self.Image.setPixmap(self.pixmap)

        self.Animation = QLabel()
        self.pixmap2 = QPixmap(self.resize_image(800,800,'Output/Animation/Animation_0.jpg','Output/Animation/Animation_0.jpg'))
        self.Animation.setPixmap(self.pixmap2)

        self.text_couleur = QLabel("Changer pour cette couleur:")
        self.text_couleur.setFont(QFont('Arial', 20))

        # Stop Button
        self.StopButton = QPushButton("Stop")
        self.StopButton.pressed.connect(self.runner.kill)

        # Pause Button
        self.PauseButton = QPushButton("Pause")
        # self.PauseButton.setGeometry(2, 2, 2, 2)
        self.PauseButton.pressed.connect(self.runner.pause)

        # Resume Button
        self.ResumeButton = QPushButton("Resume")
        self.ResumeButton.pressed.connect(self.runner.resume)

        # self.status = self.statusBar()
        self.progress = QProgressBar()
        # self.status.addPermanentWidget(self.progress)

        layout = QGridLayout()

        # Add widgets to the layout
        layout.addWidget(self.Titre, 0, 0, 1, 4)
        layout.addWidget(self.sous_titre, 1, 0, 1, 2)
        layout.addWidget(self.PauseButton, 3, 0, 1, 2)
        layout.addWidget(self.ResumeButton, 3, 2, 1, 2)
        layout.addWidget(self.progress, 2, 0, 1, 4)
        layout.addWidget(self.text_couleur, 4, 0, 1, 4)
        layout.addWidget(self.Image, 5, 0, 1, 4)
        layout.addWidget(self.Animation, 0, 5, 6, 4)

        self.setLayout(layout)

        self.Image.setHidden(True)
        self.text_couleur.setHidden(True)

        self.TotalLinesCanvas = TotalLinesCanvas

    def update_progress(self, n, color, rgb, index, CurrentNumCsvLines):
        self.progress.setValue(n)
        self.CreatePicture(rgb)
        if color:
            self.Image.setHidden(False)
            self.text_couleur.setHidden(False)
            self.pixmap = QPixmap('Output/Couleur_a_changer.png')
            self.Image.setPixmap(self.pixmap)

        else:
            self.Image.setHidden(True)
            self.text_couleur.setHidden(True)

        TrueIndex = index + (self.TotalLinesCanvas - CurrentNumCsvLines)
        path = 'Output/Animation/Animation_%i.jpg' % TrueIndex
        self.pixmap2 = QPixmap(self.resize_image(800, 800, path, path))
        self.Animation.setPixmap(self.pixmap2)

    def CreatePicture(self, rgb):
        image = Image.new("RGB", (600, 100), rgb)
        image.save('Output/Couleur_a_changer.png')

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
