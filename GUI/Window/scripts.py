# Importation des bibliothèques nécessaires
import numpy as np
import cv2
from scipy import ndimage
import math
from copy import deepcopy

# Définition de la classe Images pour le traitement d'images
class Images:
    def __init__(self, img):
        # Chargement de l'image depuis le fichier spécifié
        self.img = cv2.imread(img, 1)
        # Redimensionnement de l'image pour s'adapter à une taille prédéfinie
        if self.img.shape[0] / self.img.shape[1] < 0.76:
            self.img_width = 1100
            self.img_height = int(self.img_width * self.img.shape[0] / self.img.shape[1])
        else:
            self.img_height = 700
            self.img_width = int(self.img_height * self.img.shape[1] / self.img.shape[0])
        self.img = cv2.resize(self.img, (self.img_width, self.img_height))
        # Création d'une copie de l'image originale pour les opérations de réinitialisation
        self.img_copy = deepcopy(self.img)
        self.grand_img_copy = deepcopy(self.img)
        # Extraction du nom et du format de l'image à des fins de sauvegarde ultérieure
        self.img_name = img.split('\\')[-1].split(".")[0]
        self.img_format = img.split('\\')[-1].split(".")[1]
        # Initialisation des variables de recadrage
        self.left, self.right, self.top, self.bottom = None, None, None, None

    # Méthode pour ajuster automatiquement le contraste de l'image
    def auto_contrast(self):
        # Calcul de l'histogramme de l'image en niveaux de gris
        clip_hist_percent = 20
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)
        accumulator = [float(hist[0])]
        for index in range(1, hist_size):
            accumulator.append(accumulator[index - 1] + float(hist[index]))
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum / 100.0)
        clip_hist_percent /= 2.0
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1
        # Calcul des paramètres d'ajustement du contraste
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha
        # Application de l'ajustement du contraste à l'image
        self.img = cv2.convertScaleAbs(self.img, alpha=alpha, beta=beta)

    # Autres méthodes pour les opérations de traitement d'images...
    # (auto_sharpen, auto_cartoon, auto_invert, change_b_c, change_saturation, remove_color, crop_img, rotate_img,
    # detect_face, bypass_censorship, save_img, reset, grand_reset)

# Fonction principale pour tester la classe Images
def main():
    # Chemin de l'image à charger
    path = "ppl.jpg"
    # Création d'une instance de la classe Images avec l'image spécifiée
    img = Images(path)
    # Extraction du nom de l'image
    img_name = path.split('\\')[-1].split(".")[0]
    # Affichage de l'image dans une fenêtre OpenCV
    cv2.imshow(img_name, img.img)
    cv2.waitKey()
    cv2.destroyAllWindows()

# Vérification si le script est exécuté en tant que programme principal
if __name__ == "__main__":
    # Appel de la fonction principale pour tester la classe Images
    main()
