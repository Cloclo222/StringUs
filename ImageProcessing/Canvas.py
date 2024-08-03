import time

import numpy as np
import sys
from PIL import Image, ImageDraw, ImageFilter
# import plotly.express as px
import numba
import cv2
import imageio.v2
import os
import glob
import concurrent.futures


@numba.njit  # Ce décorateur indique que la fonction sera compilée avec le compilateur JIT de Numba pour une exécution plus rapide.
def LineSum(img, x, y):
    acc = 0  # Initialiser une variable d'accumulateur pour stocker la somme des valeurs des pixels.
    for i, j in zip(x, y):  # Parcourir les coordonnées x et y simultanément en utilisant zip.
        acc += img[j, i]  # Ajouter la valeur du pixel à la position (j, i) à l'accumulateur.
    return acc  # Renvoyer la somme accumulée.


@numba.njit
def linePixels(pin0, pin1):
    length = int(
        np.hypot(pin1[0] - pin0[0], pin1[1] - pin0[1]))  # Calcul de la longueur de la ligne utilisant l'hypoténuse
    x = np.linspace(pin0[0], pin1[0], length)  # Générer une séquence linéaire de coordonnées x entre pin0 et pin1
    y = np.linspace(pin0[1], pin1[1], length)  # Générer une séquence linéaire de coordonnées y entre pin0 et pin1
    x = np.array([int(x[i]) for i in range(len(x))]) - 1  # Convertir les coordonnées x en entiers et ajuster de -1
    y = np.array([int(y[i]) for i in range(len(y))]) - 1  # Convertir les coordonnées y en entiers et ajuster de -1
    return x, y  # Renvoyer les coordonnées x et y de la ligne


@numba.njit
def ditherImg(arr, colors_array):
    arr_shape = np.shape(arr)  # Obtenir la forme de l'array d'entrée

    num_imgs = len(colors_array)  # Nombre d'images de sortie (une par couleur dans colors_array)
    res_shape = num_imgs, arr_shape[0], arr_shape[1]  # Forme de l'array de résultat
    res_dithered = np.zeros(arr_shape)  # Initialiser l'array de résultat de la même forme que l'array d'entrée
    result_sep = np.zeros(res_shape)  # Initialiser l'array de séparation de résultat

    height, width = arr.shape[0:2]  # Obtenir la hauteur et la largeur de l'image d'entrée
    for ir in range(height):  # Boucle sur les lignes de l'image
        for ic in range(width):  # Boucle sur les colonnes de l'image
            old_val = arr[ir, ic].copy()  # Valeur de pixel d'entrée à la position (ir, ic)
            distances = np.sqrt(np.sum((colors_array - old_val) ** 2, axis=1))  # Calculer les distances aux couleurs
            closest = np.where(distances == np.amin(distances))[0][0]  # Trouver l'index de la couleur la plus proche
            new_val = colors_array[closest]  # Nouvelle valeur de pixel sélectionnée
            result_sep[
                closest, ir, ic] = 255  # Marquer la position de la couleur la plus proche dans l'array de séparation
            res_dithered[ir, ic] = new_val  # Affecter la nouvelle valeur de pixel à l'array de résultat
            err = old_val - new_val  # Calculer l'erreur de quantification

            if ic < width - 1:  # Si nous ne sommes pas à la dernière colonne
                arr[ir, ic + 1] += err * 3 / 16  # Diffuser l'erreur à la colonne suivante
            if ir < height - 1:  # Si nous ne sommes pas à la dernière ligne
                if ic > 0:
                    arr[
                        ir + 1, ic - 1] += err * 3 / 16  # Diffuser l'erreur à la colonne précédente de la ligne suivante
                arr[ir + 1, ic] += err * 5 / 16  # Diffuser l'erreur à la ligne suivante
                if ic < width - 1:
                    arr[ir + 1, ic + 1] += err / 16  # Diffuser l'erreur à la colonne suivante de la ligne suivante

    return [res_dithered, result_sep]  # Renvoyer l'array de résultat et l'array de séparation


def ComputeThreads(img, numLines, numPins, Coords, Angles, initPin=0, minLoop=3, lineWeight=10, lineWidth=10,
                   colour=(0, 0, 0)) -> []:
    # Initialize variables
    i = 0  # Variable pour compter les lignes
    lines = []  # Liste pour stocker les paires de broches formant chaque ligne
    previousPins = []  # Liste pour stocker les broches précédentes pour éviter la répétition
    oldPin = initPin  # Broche de départ
    lineMask = np.zeros_like(img)  # Masque pour soustraire la ligne de l'image

    # Boucle sur le nombre de lignes à calculer
    for line in range(numLines):
        i += 1  # Incrémenter le compteur de ligne
        bestLine = 0  # Initialiser la meilleure ligne à 0
        oldCoord = Coords[oldPin]  # Coordonnées de la broche de départ

        # Boucle sur les broches potentielles pour former la ligne
        for index in range(5, numPins - 5):
            pin = (oldPin + index) % numPins  # Calculer l'index de la broche actuelle
            lineSum = 0  # Initialiser la somme de la ligne à 0
            coord = Coords[pin]  # Coordonnées de la broche actuelle

            xLine, yLine = linePixels(oldCoord, coord)  # Obtenir les coordonnées des pixels de la ligne
            # Calculer la somme des valeurs de pixels le long de la ligne
            Sum = LineSum(img, xLine, yLine)/len(xLine)

            # Vérifier si la somme est meilleure que la meilleure ligne précédente et si la broche actuelle n'a pas déjà été utilisée
            if (Sum > bestLine) and not (pin in previousPins):
                bestLine = Sum  # Mettre à jour la meilleure ligne
                bestPin = pin  # Mettre à jour la meilleure broche

        # Mettre à jour les broches précédentes
        if len(previousPins) >= minLoop:
            previousPins.pop(0)  # Supprimer la plus ancienne broche de la liste
        previousPins.append(bestPin)  # Ajouter la meilleure broche à la liste

        # Soustraire la nouvelle ligne de l'image
        lineMask = lineMask * 0  # Réinitialiser le masque de ligne
        cv2.line(lineMask, oldCoord, Coords[bestPin], lineWeight, lineWidth)  # Dessiner la ligne sur le masque
        img = np.subtract(img, lineMask)  # Soustraire la ligne de l'image

        # Afficher la progression du calcul
        progress = img / 255
        cv2.imshow('%s' % colour, cv2.resize(progress, (400, 400)))
        cv2.waitKey(1)

        # Enregistrer la ligne dans les résultats
        lines.append((oldPin, bestPin))

        # Arrêter la boucle si aucune ligne n'est possible
        if bestPin == oldPin:
            break

        # Préparer la boucle suivante
        oldPin = bestPin  # Mettre à jour la broche de départ pour la prochaine itération

        # Afficher la progression
    #     sys.stdout.write("\b\b")
    #     sys.stdout.write("\r")
    #     sys.stdout.write("[+] Calcul de la ligne " + colour + " " + str(line + 1))
    #     sys.stdout.flush()
    #
    # sys.stdout.write("\n")
    cv2.destroyAllWindows()  # Fermer toutes les fenêtres d'affichage
    return lines  # Renvoyer les lignes calculées


def WriteThreadedCsvFile(filename, lines, imgRadius=1000):
    csv_output = open(filename, 'wb')  # Ouvrir le fichier CSV en mode écriture binaire
    csv_output.write("p1,p2,R,G,B\n".encode('utf8'))  # Écrire l'en-tête du fichier CSV

    # Fonction lambda pour formater les lignes de données en CSV
    csver = lambda p1, p2, R, G, B: "%i" % p1 + "," + "%i" % p2 + "," + "%i" % R + "," + "%i" % G + "," + "%i" % B + "\n"

    # Boucle sur les lignes de données et écrire dans le fichier CSV
    for l in lines:
        csv_output.write(csver(l[0][0], l[0][1], l[1][0], l[1][1], l[1][2]).encode('utf8'))

    csv_output.close()  # Fermer le fichier CSV


class Canvas:
    def __init__(self,
                 filename,
                 img_radius=1000,
                 numPins=250,
                 initPin=0,
                 lineWidth=10,
                 lineWeight=10,
                 minLoop=3,
                 palette=None,
                 numLinesPerColour=None,
                 group_orders=None,
                 fillColor=(255, 255, 255),
                 Topleftpixel=(0, 0),
                 CropDiameter=1000
                 ):
        """
        Initialisateur de la classe Canvas.

        Paramètres :
            - filename : Le nom du fichier de l'image.
            - img_radius : Le rayon de l'image.
            - numPins : Le nombre de broches.
            - initPin : La broche initiale.
            - lineWidth : La largeur de la ligne.
            - lineWeight : Le poids de la ligne.
            - minLoop : Le nombre minimal d'itérations.
            - palette : La palette de couleurs.
            - numLinesPerColour : Le nombre de lignes par couleur.
            - group_orders : Les ordres de groupe.
            - fillColor : La couleur de remplissage.
            - Topleftpixel : Le pixel en haut à gauche.
            - CropDiameter : Le diamètre de recadrage.
        """
        self.numLinesPerColour = numLinesPerColour
        self.filename = filename
        self.img_radius = img_radius
        self.numPins = numPins
        self.initPin = initPin
        self.lineWidth = lineWidth
        self.lineWeight = lineWeight
        self.minLoop = minLoop
        self.Coords = None
        self.Angles = None
        self.img_dithered = None

        self.totalLines = None

        # Charger l'image et initialiser les attributs en fonction des paramètres
        self.base_img = Image.open(self.filename, ).convert('RGB').resize(
            (self.img_radius * 2 + 1, self.img_radius * 2 + 1))

        self.pinCoords(numPins=self.numPins)

        # Créer l'image dithered si une palette est fournie, sinon convertir l'image en niveaux de gris
        if palette is not None:
            self.greyscale = False
            if numLinesPerColour is None:
                self.numLinesPerColour = dict()
                for key in palette.keys():
                    self.numLinesPerColour[key] = 100000
            else:
                assert set(palette.keys()) == set(
                    numLinesPerColour.keys()), "Les clés de la palette et de numLinesPerColour ne correspondent pas"
            self.palette = palette
            self.colors_array = np.array(list(self.palette.values()))
            self.np_img = np.array(self.base_img, dtype=float)
            self.img_couleur_sep = dict()
            self.d_couleur_threaded = dict()

            self.color_names = list(self.palette.keys())
            self.color_values = list(self.palette.values())

            first_color_letters = [color[1] for color in self.color_names]
            assert len(set(first_color_letters)) == len(
                first_color_letters), "La première lettre de chaque nom de couleur doit être unique."
            # assert set(first_color_letters) == set(group_orders), "Lettre invalide dans group_order"
            self.group_orders = group_orders

            for keys in self.palette.keys():
                self.img_couleur_sep[keys] = np.zeros(self.np_img.shape[:2])

            # self.maskImage()
            self.fs_dither()

        else:
            self.np_img = np.array(self.base_img.convert('L'), dtype=float)
            self.invertImage()
            self.img_couleur_sep = dict(
                grey=self.np_img
            )
            self.greyscale = True
            # Image.fromarray(self.img).show()

    def pinCoords(self, numPins, offset=0, x0=None, y0=None):
        """
        Méthode pour calculer les coordonnées des broches.

        Paramètres :
            - numPins : Le nombre de broches.
            - offset : Le décalage d'angle.
            - x0 : La coordonnée x du centre de l'image.
            - y0 : La coordonnée y du centre de l'image.
        """
        self.numPins = numPins
        alpha = np.linspace(0 + offset, 2 * np.pi + offset, self.numPins + 1)

        if (x0 is None) or (y0 is None):
            x0 = self.img_radius + 1
            y0 = self.img_radius + 1

        coords = []
        for angle in alpha[0:-1]:
            x = int(x0 + self.img_radius * np.cos(angle))
            y = int(y0 + self.img_radius * np.sin(angle))

            coords.append((x, y))
        self.Coords = coords
        self.Angles = alpha[0:-1]

    def helper(self, colour):
        return ComputeThreads(self.img_couleur_sep[colour],
                              numLines=self.numLinesPerColour[colour],
                              numPins=self.numPins,
                              Coords=self.Coords,
                              Angles=self.Angles,
                              initPin=self.initPin,
                              lineWidth=self.lineWidth,
                              lineWeight=self.lineWeight,
                              colour=colour)
    def buildCanvas(self, numLines=10000, background=(255, 255, 255), excludeBackground=False):
        """
        Méthode pour construire le canvas.

        Paramètres :
            - numLines : Le nombre de lignes à créer.
            - background : La couleur de fond.
            - excludeBackground : Indicateur pour exclure le fond lors de la création des lignes.
        """
        self.totalLines = []
        if self.greyscale is True:
            # assert numLines != 0, "Doit spécifier le nombre de lignes dans buildCanvas, pour Greyscale"
            Lines = ComputeThreads(self.img_couleur_sep["grey"],
                                   numLines=numLines,
                                   numPins=self.numPins,
                                   Coords=self.Coords,
                                   Angles=self.Angles,
                                   initPin=self.initPin,
                                   lineWidth=self.lineWidth,
                                   lineWeight=self.lineWeight,
                                   colour='black')
            Lines = np.flipud(Lines)
            print("\n[+] Image threaded")
            # for line in enumerate(Lines):
            #     self.totalLines[i] = [line, "black"]
            z = [(0, 0, 0) for i in range(len(Lines))]
            self.totalLines = list(zip(Lines, z))

        else:
            s = time.time()
            MP = True
            if MP:
                with concurrent.futures.ProcessPoolExecutor() as pool:
                    results = pool.map(self.helper, self.palette.keys())
                for (key, result) in zip(self.palette.keys(), results):
                    self.d_couleur_threaded[key] = np.flip(result)
            else:
                for key in self.palette.keys():
                    if self.palette[key] == background and excludeBackground is True:
                        continue
                    else:
                        self.d_couleur_threaded[key] = ComputeThreads(self.img_couleur_sep[key],
                                                                      numLines=self.numLinesPerColour[key],
                                                                      numPins=self.numPins,
                                                                      Coords=self.Coords,
                                                                      Angles=self.Angles,
                                                                      initPin=self.initPin,
                                                                      lineWidth=self.lineWidth,
                                                                      lineWeight=self.lineWeight,
                                                                      colour=key)
                        self.d_couleur_threaded[key] = np.flip(self.d_couleur_threaded[key])
                        print("Threaded %i %s lines" % (len(self.d_couleur_threaded[key]), key))

            e = time.time()
            self.OrderColours(background, excludeBackground)

            print(f"[+] Image threaded in {e-s}s\n")

    def OrderColours(self, background=(255, 255, 255), excludeBackground=False):
        """
        Méthode pour ordonner les couleurs.

        Paramètres :
            - background : La couleur de fond.
            - excludeBackground : Indicateur pour exclure le fond lors de l'ordonnancement des couleurs.
        """
        self.totalLines = []
        color_names = list(self.palette.keys())
        color_counters = {k: 0 for k in color_names}
        matching_rgb = list(self.palette.values())

        for g in self.group_orders.split():
            num_instances = len([c for c in self.group_orders.split() if c == g])
            matching_color = [c for c in color_names if c == g][0]
            if self.palette[matching_color] == background and excludeBackground is True:
                continue
            else:
                color_value = self.palette[matching_color]
                color_counters[matching_color] += 1
                color_len = len(self.d_couleur_threaded[matching_color])
                start = int(color_len * (color_counters[matching_color] - 1) / num_instances)
                end = int(color_len * color_counters[matching_color] / num_instances)
                next_lines = self.d_couleur_threaded[matching_color][start: end]
                for line in next_lines:
                    self.totalLines.append((line, color_value))

    def paintCanvas(self, background=(255, 255, 255)):
        """
        Méthode pour peindre le canvas.

        Paramètres :
            - background : La couleur de fond.
        """
        if self.greyscale is False:
            output = Image.new('RGB', (self.img_radius * 2, self.img_radius * 2), background)
            outputDraw = ImageDraw.Draw(output)
            for line in self.totalLines:
                pin1 = line[0][0]
                pin2 = line[0][1]
                colour = line[-1]
                outputDraw.line((self.Coords[pin1], self.Coords[pin2]), fill=colour)
        else:
            output = Image.new('L', (self.img_radius * 2, self.img_radius * 2), 255)
            outputDraw = ImageDraw.Draw(output)
            for line in self.totalLines:
                pin1 = line[0][0]
                pin2 = line[0][1]
                colour = 0
                outputDraw.line((self.Coords[pin1], self.Coords[pin2]), fill=colour)
        return output

    def fs_dither(self):
        """
        Méthode pour effectuer le dithering Floyd-Steinberg.
        """
        res = ditherImg(self.np_img, self.colors_array)
        self.img_dithered = np.array(res[0])
        for i, key in enumerate(self.palette.keys()):
            img_blur = cv2.blur(res[1][i], (3, 3))
            # cv2.imshow('', img_blur/255)
            # cv2.waitKey(0)
            # self.img_couleur_sep[key] = img_blur
            self.img_couleur_sep[key] = res[1][i]

    # Invert grayscale image
    def invertImage(self):
        """
        Méthode pour inverser l'image en niveaux de gris.
        """
        self.np_img = 255 - self.np_img

    # def showDitheredImage(self):
    #     """
    #     Méthode pour afficher l'image dithered.
    #     """
    #     px.imshow(self.img_dithered, template="plotly_dark").show()
    #     fig = px.imshow(
    #         np.array(list(self.img_couleur_sep.values())), template="plotly_dark",
    #         title="Images par couleur", animation_frame=0, color_continuous_scale="gray"
    #     ).update_layout(coloraxis_showscale=False)
    #     fig.layout.sliders[0].currentvalue.prefix = "couleur = "
    #     for i, color_name in enumerate(self.palette.keys()):
    #         fig.layout.sliders[0].steps[i].label = color_name
    #     fig.show()

    def getNumLines(self):
        """
        Méthode pour obtenir le nombre total de lignes.
        """
        return len(self.totalLines)

    def animate(self, fps):
        """
        Méthode pour générer une animation avec les images de l'animation.

        Paramètres :
            - fps : Les images par seconde de l'animation.
        """
        if os.path.exists('Output/Animation') is False:
            os.makedirs('Output/Animation')
        if os.path.exists('Output/Videos_Animation') is False:
            os.makedirs('Output/Videos_Animation')

        files = glob.glob('Output/Animation/*')
        for f in files:
            os.remove(f)

        output = Image.new('RGB', (self.img_radius * 2, self.img_radius * 2), (188, 188, 175))
        outputDraw = ImageDraw.Draw(output)

        writer = imageio.get_writer('Output/Videos_Animation/Animation.avi', fps=fps)

        for i in range(len(self.totalLines)):
            outputDraw.line((self.Coords[self.totalLines[i][0][0]], self.Coords[self.totalLines[i][0][1]]),
                            fill=self.totalLines[i][-1], width=2)
            output.save("Output/Animation/Animation_%i.jpg" % i)
            writer.append_data(np.array(output))
            print("1")
        writer.close()
        print("done animation")

    def generateImgs(self):
        """
        Méthode pour générer des images de la simulation
        """
        if os.path.exists('Output/Animation') is False:
            os.makedirs('Output/Animation')

        files = glob.glob('Output/Animation/*')
        for f in files:
            os.remove(f)

        output = Image.new('RGB', (self.img_radius * 2, self.img_radius * 2), (188, 188, 175))
        outputDraw = ImageDraw.Draw(output)

        for i in range(len(self.totalLines)):
            outputDraw.line((self.Coords[self.totalLines[i][0][0]], self.Coords[self.totalLines[i][0][1]]),
                            fill=self.totalLines[i][-1], width=2)
            if i % 2 == 0:
                output.save("Output/Animation/Animation_%i.jpg" % i)
