import PIL.Image
import numpy as np
import sys
from PIL import Image
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Img:

    def __init__(self, filename, palette = None, img_radius=1000):
        self.filename = filename
        self.img_radius = img_radius



        if palette is not None:
            self.palette = palette
            self.img = np.array(Image.open(self.filename).resize((self.img_radius * 2 + 1, self.img_radius * 2 + 1)),dtype=float)
            self.img_couleur_sep = dict()
            for keys in self.palette.keys():
                self.img_couleur_sep[keys] = np.zeros(self.img.shape[:2])

            # self.maskImage()
            self.img_dithered = self.fs_dither()
        else:
            self.img = np.array(Image.open(self.filename).resize((self.img_radius * 2 + 1, self.img_radius * 2 + 1)).convert('L'),dtype=float)
            self.invertImage()
            # Image.fromarray(self.img).show()
    def GetClosestPaletteColour(self, old_val):
        colours = list(self.palette.values())
        #colours = np.array(colours)
        distances = np.sqrt(np.sum((colours - old_val) ** 2, axis=1))
        closest = np.where(distances == np.amin(distances))[0][0]
        colour = list(self.palette.keys())[list(self.palette.values()).index(colours[closest])]
        return colour

    def fs_dither(self):
        arr = self.img
        height, width = arr.shape[0:2]
        for ir in range(height):
            for ic in range(width):
                old_val = arr[ir, ic].copy()
                new_colour = self.GetClosestPaletteColour(old_val)
                new_val = self.palette[new_colour]
                self.img_couleur_sep[new_colour][ir][ic] = 255
                arr[ir, ic] = new_val
                err = old_val - new_val

                if ic < width - 1:
                    arr[ir, ic + 1] += err * 3 / 16
                if ir < height - 1:
                    if ic > 0:
                        arr[ir + 1, ic - 1] += err * 3 / 16
                    arr[ir + 1, ic] += err * 5 / 16
                    if ic < width - 1:
                        arr[ir + 1, ic + 1] += err / 16

            sys.stdout.write("\b\b")
            sys.stdout.write("\r")
            sys.stdout.write("[+] Dithering " + str(int(ir/height*100)) + "% complete")
            sys.stdout.flush()
        # carr = np.array(arr / np.max(arr, axis=(0, 1)) * 255, dtype=np.uint8)
        return arr

    #
    # def imagePreProcessing(self):
    #     #  Crop image
    #     height, width = self.img.shape[0:2]
    #     minEdge = min(height, width)
    #     topEdge = int((height - minEdge) / 2)
    #     leftEdge = int((width - minEdge) / 2)
    #     imgCropped = self.img[topEdge:topEdge + minEdge, leftEdge:leftEdge + minEdge]
    #
    #     # Resize image
    #     imgSized = cv2.resize(imgCropped, (2 * imgRadius + 1, 2 * imgRadius + 1))
    #     return imgSized

    # Invert grayscale image
    def invertImage(self):
        self.img = 255-self.img

    # Apply circular mask to image
    def maskImage(self):
        radius = self.img_radius
        y, x = np.ogrid[-radius:radius, -radius:radius]
        mask = x ** 2 + y ** 2 > radius ** 2
        self.img[mask] = 0

    def showImage(self):
        px.imshow(self.img, template="plotly_dark").show()
        fig = px.imshow(
            np.array(list(self.img_couleur_sep.values())), template="plotly_dark",
            title="Images per color", animation_frame=0, color_continuous_scale="gray"
        ).update_layout(coloraxis_showscale=False)
        fig.layout.sliders[0].currentvalue.prefix = "color = "
        for i, color_name in enumerate(self.palette.keys()):
            fig.layout.sliders[0].steps[i].label = color_name
        fig.show()