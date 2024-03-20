# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from widgets import *


class Main(QWidget):
    def __init__(self, files):
        # initialize
        super().__init__()
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\ui\\main.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\icon\\icon.png"))
        self.move(120, 100)
        self.img_list, self.rb = [], None
        for f in files:
            self.img_list.append(Images(f))
        self.img_id = 0
        self.img_class = self.img_list[self.img_id]
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))


        self.adjust_btn = self.findChild(QPushButton, "adjust_btn")
        self.adjust_btn.clicked.connect(self.adjust_frame)
 
        self.save_btn = self.findChild(QPushButton, "save_btn")
        self.save_btn.clicked.connect(self.click_save)


        # display img
        self.gv = self.findChild(QGraphicsView, "gv")
        self.scene = QGraphicsScene()
        self.scene_img = self.scene.addPixmap(self.img)
        self.gv.setScene(self.scene)

        # zoom in
        self.zoom_moment = False
        self._zoom = 0

        # misc
        self.rotate_value, self.brightness_value, self.contrast_value, self.saturation_value = 0, 0, 1, 0
        self.flip = [False, False]
        self.zoom_factor = 1

    def update_img(self, movable=False):
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))
        self.scene.removeItem(self.scene_img)
        self.scene_img = self.scene.addPixmap(self.img)
        if movable:
            self.scene_img.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self.fitInView()

    def get_zoom_factor(self):
        return self.zoom_factor

    def adjust_frame(self):
        adjust_frame = Adjust(self)
        self.base_frame.setParent(None)
        self.vbox.addWidget(adjust_frame.frame)

    def click_save(self):
        try:
            file, _ = QFileDialog.getSaveFileName(self, 'Save File', f"{self.img_class.img_name}."
                                                                     f"{self.img_class.img_format}",
                                                  "Image Files (*.jpg *.png *.jpeg *.ico);;All Files (*)")
            self.img_class.save_img(file)
        except Exception:
            pass

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


def main():
    app = QApplication(sys.argv)
    lol = ["C:/Users/Xavier Lefebvre/20200211_164050.jpg"]
    window = Main(lol)
    #window = Start()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
