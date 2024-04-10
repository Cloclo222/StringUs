# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from .widgets import *

class Crop(QWidget):
    def __init__(self, files):
        # initialise la classe Crop
        super().__init__()
        # Charge l'interface utilisateur depuis le fichier main.ui
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\main.ui", self)
        # Définit l'icône de la fenêtre
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\icon\\icon.png"))
        # Déplace la fenêtre à la position (120, 100) sur l'écran
        self.move(120, 100)
        # Initialise une liste d'images et un radiobouton
        self.img_list, self.rb = [], None
        # Pour chaque fichier d'image fourni, crée un objet Images et l'ajoute à la liste d'images
        for f in files:
            self.img_list.append(Images(f))
        # Initialise l'ID de l'image actuelle à 0 et récupère l'objet Images correspondant
        self.img_id = 0
        self.img_class = self.img_list[self.img_id]
        # Convertit l'image en pixmap pour affichage dans une QGraphicsScene
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))

        # Connexion des signaux des boutons
        self.adjust_btn = self.findChild(QPushButton, "adjust_btn")
        self.adjust_btn.clicked.connect(self.adjust_frame)
        self.save_btn = self.findChild(QPushButton, "save_btn")
        self.save_btn.clicked.connect(self.click_save)

        # Affichage de l'image dans QGraphicsView
        self.gv = self.findChild(QGraphicsView, "gv")
        self.scene = QGraphicsScene()
        self.scene_img = self.scene.addPixmap(self.img)
        self.gv.setScene(self.scene)

        # Zoom
        self.zoom_moment = False
        self._zoom = 0

        # Autres attributs pour ajuster l'image
        self.rotate_value, self.brightness_value, self.contrast_value, self.saturation_value = 0, 0, 1, 0
        self.flip = [False, False]
        self.zoom_factor = 1

    # Met à jour l'image affichée
    def update_img(self, movable=False):
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))
        self.scene.removeItem(self.scene_img)
        self.scene_img = self.scene.addPixmap(self.img)
        if movable:
            self.scene_img.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self.fitInView()

    # Renvoie le facteur de zoom actuel
    def get_zoom_factor(self):
        return self.zoom_factor

    # Ouvre une fenêtre pour ajuster l'image
    def adjust_frame(self):
        adjust_frame = Adjust(self)
        self.base_frame.setParent(None)
        self.vbox.addWidget(adjust_frame.frame)

    # Sauvegarde l'image
    def click_save(self):
        try:
            self.img_class.save_img()
            self.close()
        except Exception:
            pass

    # Gère l'événement de roulette de la souris pour le zoom
    def wheelEvent(self, event):
        if self.zoom_moment:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.gv.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    # Ajuste la vue pour afficher toute l'image
    def fitInView(self):
        rect = QRectF(self.img.rect())
        if not rect.isNull():
            self.gv.setSceneRect(rect)
            unity = self.gv.transform().mapRect(QRectF(0, 0, 1, 1))
            self.gv.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.gv.viewport().rect()
            scene_rect = self.gv.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.gv.scale(factor, factor)
            self._zoom = 0
            self.zoom_factor = factor



