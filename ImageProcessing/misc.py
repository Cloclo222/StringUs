import itertools

#from Canvas import *
import numpy as np
import os
import cv2


def centerImg(filename, fillColor=(255, 255, 255), Topleftpixel=(0, 0), imgDiameter=1000):
    # Ouvrir l'image à partir du fichier spécifié et la convertir en mode RGB
    img = Image.open(filename).convert('RGB')
    # Convertir l'image en tableau numpy pour la manipulation
    img = np.array(img)

    # Créer une image avec des dimensions spécifiées et remplie avec la couleur spécifiée
    img_cropped = (np.ones((imgDiameter, imgDiameter, 3)) * fillColor)

    # Détermination de la région à extraire de l'image source pour la placer au centre de l'image recadrée

    # Déterminer les coordonnées de début et de fin de la région de l'image source à extraire
    rowStart = Topleftpixel[0] if Topleftpixel[0] >= 0 else 0
    colomnStart = Topleftpixel[1] if Topleftpixel[1] >= 0 else 0
    rowEnd = img.shape[0] if (imgDiameter + Topleftpixel[0]) > img.shape[0] else (imgDiameter + Topleftpixel[0])
    colomnEnd = img.shape[1] if (imgDiameter + Topleftpixel[1]) > img.shape[1] else (imgDiameter + Topleftpixel[1])

    # Détermination des coordonnées de début et de fin de la région recadrée dans l'image résultante

    # Calculer les coordonnées de début de la région recadrée dans l'image résultante
    rowStartCropped = np.abs(Topleftpixel[0]) if not Topleftpixel[0] >= 0 else 0
    colomnStartCropped = np.abs(Topleftpixel[1]) if not Topleftpixel[1] >= 0 else 0

    # Calculer les coordonnées de fin de la région recadrée dans l'image résultante
    rowEndcropped = imgDiameter if imgDiameter < img.shape[0] - Topleftpixel[0] else img.shape[0] - Topleftpixel[0]
    colomnEndcropped = imgDiameter if imgDiameter < img.shape[1] - Topleftpixel[1] else img.shape[1] - Topleftpixel[1]

    # Copier la région de l'image source dans la région spécifiée de l'image recadrée
    img_cropped[rowStartCropped:rowEndcropped, colomnStartCropped:colomnEndcropped] = img[rowStart:rowEnd,
                                                                                      colomnStart:colomnEnd]
    # Convertir le tableau numpy résultant en une image PIL
    img_cropped = Image.fromarray(img_cropped.astype(np.uint8))

    # Retourner l'image recadrée
    return img_cropped



def animate(lines, coords, imgRadius):
    """
    Fonction pour animer le dessin des lignes.

    Paramètres :
        - lines : Liste de tuples représentant les lignes à dessiner. Chaque tuple contient l'indice de début de la ligne, l'indice de fin de la ligne et la couleur de la ligne.
        - coords : Liste des coordonnées des points de dessin.
        - imgRadius : Rayon de l'image.

    Cette fonction dessine progressivement les lignes spécifiées dans l'image en utilisant les coordonnées fournies, en affichant chaque étape de dessin pendant un court laps de temps.
    """
    # Création d'une image vide pour afficher le dessin
    imgResult = np.ones((imgRadius * 2, imgRadius * 2, 3)) * 125

    # Boucle sur chaque ligne à dessiner
    for l in lines:
        # Obtenir les coordonnées des pixels de la ligne à dessiner
        xLine, yLine = linePixels(coords[l[0]], coords[l[1]])

        # Dessiner la ligne dans l'image de résultat avec la couleur spécifiée
        imgResult[yLine, xLine] = l[2]

        # Afficher l'image avec la ligne dessinée
        cv2.imshow('image', imgResult)
        cv2.waitKey(1)  # Attendre un court laps de temps pour afficher l'image (rafraîchissement)

    cv2.waitKey(0)  # Attendre indéfiniment jusqu'à ce qu'une touche soit pressée pour terminer l'animation
    cv2.destroyAllWindows()  # Fermer les fenêtres OpenCV



def WriteThreadedCsvFile(filename, lines, imgRadius=1000):
    """
    Fonction pour écrire les données des lignes dans un fichier CSV.

    Paramètres :
        - filename : Nom du fichier CSV à créer.
        - lines : Liste de tuples représentant les lignes. Chaque tuple contient deux tuples représentant les points de début et de fin de la ligne, ainsi que les valeurs RGB de la couleur de la ligne.
        - imgRadius : Rayon de l'image.

    Cette fonction crée un fichier CSV contenant les données des lignes spécifiées. Chaque ligne du fichier CSV contient les coordonnées des deux points de la ligne (p1, p2) ainsi que les valeurs R, G, B de la couleur de la ligne.
    """
    # Ouvrir le fichier CSV en mode écriture binaire
    csv_output = open(filename, 'wb')

    # Écrire l'en-tête du fichier CSV
    csv_output.write("p1,p2,R,G,B\n".encode('utf8'))

    # Fonction lambda pour formater les données de ligne en chaîne CSV
    csver = lambda p1, p2, R, G, B: "%i" % p1 + "," + "%i" % p2 + "," + "%i" % R + "," + "%i" % G + "," + "%i" % B + "\n"

    # Boucler sur chaque ligne et écrire ses données dans le fichier CSV
    for l in lines:
        csv_output.write(csver(l[0][0], l[0][1], l[1][0], l[1][1], l[1][2]).encode('utf8'))

    # Fermer le fichier CSV après écriture
    csv_output.close()



def createGrid(folder=None):
    """
    Fonction pour créer une grille d'images à partir d'un dossier d'images.

    Paramètres :
        - folder : Nom du dossier contenant les images. Si non spécifié, le dossier par défaut est utilisé.

    Cette fonction parcourt un dossier d'images, redimensionne chaque image pour avoir la même taille, puis les organise en une grille d'images avec une marge spécifiée entre chaque image. La grille est ensuite enregistrée dans un fichier JPEG.
    """
    # Variables définies par l'utilisateur
    dirname = "imgs/tiger_ratio"  # Nom du répertoire contenant les images
    name = "outputs/tiger_grid" + ".jpg"  # Nom du fichier exporté
    margin = 20  # Marge entre les images en pixels
    w = 5  # Largeur de la matrice (nombre d'images)
    h = 5  # Hauteur de la matrice (nombre d'images)
    n = w * h

    filename_list = []

    # Parcourir les fichiers dans le dossier spécifié
    for file in os.listdir(dirname):
        filename_list.append(file)

    filename_list.sort()

    print(filename_list)

    # Charger et redimensionner les images
    imgs = [cv2.resize(cv2.imread(os.getcwd() + "/" + dirname + "/" + file), (1000, 1000), interpolation=cv2.INTER_AREA)
            for file in filename_list]

    # Définir la forme de l'image à répliquer (toutes les images doivent avoir la même forme)
    img_h, img_w, img_c = imgs[0].shape

    # Définir les marges dans les directions x et y
    m_x = margin
    m_y = margin

    # Taille de l'image complète
    mat_x = img_w * w + m_x * (w - 1)
    mat_y = img_h * h + m_y * (h - 1)

    # Créer une matrice de zéros de la bonne taille et la remplir avec 255 (pour que les marges soient blanches)
    imgmatrix = np.ones((mat_y, mat_x, img_c), np.uint8) * 255

    # Préparer un itérable avec les bonnes dimensions
    positions = itertools.product(range(h), range(w))

    # Placer chaque image dans la grille
    for (y_i, x_i), img in zip(positions, imgs):
        x = x_i * (img_w + m_x)
        y = y_i * (img_h + m_y)
        imgmatrix[y:y + img_h, x:x + img_w, :] = img

    # Redimensionner l'image de la grille et l'enregistrer dans un fichier JPEG
    resized = cv2.resize(imgmatrix, (mat_x, mat_y), interpolation=cv2.INTER_AREA)
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, 90]
    cv2.imwrite(name, resized, compression_params)


