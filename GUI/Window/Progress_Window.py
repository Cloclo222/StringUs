# Importation des modules nécessaires
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import (
    QObject, pyqtSlot, QRunnable, QThreadPool
)
from PyQt5 import QtCore as qtc
from stringus_code_IDE.SCARA_COM import *  # Importation de la classe SCARA_COM depuis un module externe
from ImageProcessing.Canvas import *  # Importation d'une classe Canvas depuis un module externe


# Définition d'une classe pour les signaux utilisés par le worker
class WorkerSignals(QObject):
    progress = qtc.pyqtSignal(int, bool, tuple, int, int)  # Signal pour la progression avec différents arguments
    # color = qtc.pyqtSignal(bool)


# Définition d'une classe pour le travail à effectuer en arrière-plan
class JobRunner(QRunnable):
    signals = WorkerSignals()  # Instanciation de la classe pour les signaux

    def __init__(self, filename, nb_clous, TotalLinesCanvas, portArduino):
        super().__init__()

        # Initialisation des attributs avec les paramètres passés
        self.TotalLinesCanvas = TotalLinesCanvas
        self.filename = filename
        self.is_paused = False
        self.is_killed = False
        self.scara_com = SCARA_COM(portArduino)  # Instanciation de la classe SCARA_COM avec un paramètre
        self.scara_com.readThreadedCSV(filename, nb_clous)  # Lecture du fichier CSV avec la classe SCARA_COM
        self.NumCSVLines = self.scara_com.getNumLinesCSV()  # Obtention du nombre de lignes dans le CSV
        self.need_change = False  # Initialisation d'un drapeau pour indiquer s'il faut changer de couleur

    @pyqtSlot()
    def run(self):
        # Boucle sur les commandes à exécuter
        for index, cmd in enumerate(self.scara_com.commandes):
            # Calcul du pourcentage de progression
            percent = int(((index + (self.TotalLinesCanvas - self.NumCSVLines)) / (self.TotalLinesCanvas)) * 100)
            # Émission du signal de progression avec les arguments appropriés
            self.signals.progress.emit(percent, self.need_change, self.scara_com.pinColours[index], index,
                                       self.NumCSVLines)

            # Vérification des conditions pour changer de couleur
            if index == 0:
                self.need_change = True
                self.is_paused = True
                self.signals.progress.emit(percent, self.need_change, self.scara_com.pinColours[index], index,
                                           self.NumCSVLines)

            # Envoi de la commande au SCARA et mise à jour de la progression
            self.scara_com.send_one_line(index, cmd)
            self.EraseCSVLine()
            time.sleep(0.1)

            # Vérification si la couleur a changé
            if self.scara_com.pinColours[index] != self.scara_com.pinColours[index - 1] and index > 0:
                self.need_change = True
                self.is_paused = True
                self.signals.progress.emit(percent, self.need_change, self.scara_com.pinColours[index], index,
                                           self.NumCSVLines)

            # Attente si le travail est en pause
            while self.is_paused:
                time.sleep(0)

            # Réinitialisation du drapeau pour changer de couleur
            self.need_change = False

            # Arrêt si le travail est annulé
            if self.is_killed:
                break

    # Méthode pour créer une image avec une couleur spécifique
    def CreatePicture(self, rgb):
        image = Image.new("RGB", (100, 100), rgb)
        image.save('Output/Couleur_a_changer.png')

    # Méthode pour mettre en pause le travail
    def pause(self):
        self.is_paused = True

    # Méthode pour reprendre le travail
    def resume(self):
        self.is_paused = False

    # Méthode pour arrêter le travail
    def kill(self):
        self.is_killed = True

    # Méthode pour effacer une ligne du fichier CSV
    def EraseCSVLine(self):
        df = pd.read_csv(self.filename)
        df = df.drop(0)
        df.to_csv(self.filename, index=False)


# Définition d'une classe pour la fenêtre d'affichage de la progression
class Window_Progress(QWidget):

    def __init__(self, filename, nb_clous, TotalLinesCanvas, portArduino):
        super().__init__()

        # Configuration de la fenêtre
        self.setWindowTitle("Information Robot")
        self.setGeometry(100, 100, 500, 500)

        # Création des widgets
        self.Titre = QLabel("STRINGUS: Du virtuel au réel")
        self.Titre.setFont(QFont('Arial', 30))
        self.sous_titre = QLabel("Information Robot")
        self.sous_titre.setFont(QFont('Arial', 20))
        self.threadpool = QThreadPool()  # Création d'un pool de threads
        self.runner = JobRunner(filename, nb_clous, TotalLinesCanvas,portArduino)  # Création d'un travail en arrière-plan
        self.runner.signals.progress.connect(self.update_progress)  # Connexion du signal de progression à une méthode
        self.threadpool.start(self.runner)  # Démarrage du travail en arrière-plan
        self.Image = QLabel()  # Création d'un label pour afficher une image
        self.pixmap = QPixmap('Output/Couleur_a_changer.png')  # Chargement d'une image
        self.Image.setPixmap(self.pixmap)  # Affichage de l'image
        self.Animation = QLabel()  # Création d'un label pour afficher une animation
        self.pixmap2 = QPixmap(self.resize_image(800, 800, 'Output/Animation/Animation_0.jpg',
                                                 'Output/Animation/Animation_0.jpg'))  # Chargement d'une animation
        self.Animation.setPixmap(self.pixmap2)  # Affichage de l'animation
        self.text_couleur = QLabel("Changer pour cette couleur:")  # Création d'un label de texte
        self.text_couleur.setFont(QFont('Arial', 20))  # Configuration de la police de caractères
        self.StopButton = QPushButton("Stop")  # Création d'un bouton pour arrêter le travail
        self.StopButton.pressed.connect(self.runner.kill)  # Connexion du signal pressé à une méthode
        self.PauseButton = QPushButton("Pause")  # Création d'un bouton pour mettre en pause le travail
        self.PauseButton.pressed.connect(self.runner.pause)  # Connexion du signal pressé à une méthode
        self.ResumeButton = QPushButton("Resume")  # Création d'un bouton pour reprendre le travail
        self.ResumeButton.pressed.connect(self.runner.resume)  # Connexion du signal pressé à une méthode
        self.progress = QProgressBar()  # Création d'une barre de progression
        layout = QGridLayout()  # Création d'une mise en page

        # Ajout des widgets à la mise en page
        layout.addWidget(self.Titre, 0, 0, 1, 4)
        layout.addWidget(self.sous_titre, 1, 0, 1, 2)
        layout.addWidget(self.PauseButton, 3, 0, 1, 2)
        layout.addWidget(self.ResumeButton, 3, 2, 1, 2)
        layout.addWidget(self.progress, 2, 0, 1, 4)
        layout.addWidget(self.text_couleur, 4, 0, 1, 4)
        layout.addWidget(self.Image, 5, 0, 1, 4)
        layout.addWidget(self.Animation, 0, 5, 6, 4)
        self.setLayout(layout)  # Définition de la mise en page

        # Configuration de la visibilité des widgets
        self.Image.setHidden(True)
        self.text_couleur.setHidden(True)

        self.TotalLinesCanvas = TotalLinesCanvas  # Assignation du nombre total de lignes du canevas

    def closeEvent(self, event):
        print("Widget is closing")
        self.runner.scara_com.arduino.close()
        super().closeEvent(event)

    # Méthode pour mettre à jour la progression
    def update_progress(self, n, color, rgb, index, CurrentNumCsvLines):
        self.progress.setValue(n)  # Définition de la valeur de la barre de progression
        self.CreatePicture(rgb)  # Création d'une image avec une couleur spécifique
        if color:
            self.Image.setHidden(False)  # Affichage de l'image
            self.text_couleur.setHidden(False)  # Affichage du texte
            self.pixmap = QPixmap('Output/Couleur_a_changer.png')  # Chargement de l'image
            self.Image.setPixmap(self.pixmap)  # Affichage de l'image
        else:
            self.Image.setHidden(True)  # Masquage de l'image
            self.text_couleur.setHidden(True)  # Masquage du texte

        # Calcul de l'index réel
        TrueIndex = index + (self.TotalLinesCanvas - CurrentNumCsvLines)
        path = 'Output/Animation/Animation_%i.jpg' % TrueIndex
        self.pixmap2 = QPixmap(self.resize_image(800, 800, path, path))  # Chargement de l'animation
        self.Animation.setPixmap(self.pixmap2)  # Affichage de l'animation

    # Méthode pour créer une image avec une couleur spécifique
    def CreatePicture(self, rgb):
        image = Image.new("RGB", (600, 100), rgb)
        image.save('Output/Couleur_a_changer.png')  # Sauvegarde de l'image

    # Méthode pour redimensionner une image
    def resize_image(self, largeur, hauteur, image_path, save_as):

        image = Image.open(image_path)  # Ouverture de l'image
        resized = image.resize((largeur, hauteur))  # Redimensionnement de l'image

        # Sauvegarde de l'image redimensionnée
        resized.save(save_as)

        return save_as
