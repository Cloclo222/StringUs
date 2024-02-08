import numpy as np
import sys
from PIL import Image, ImageDraw
import plotly.express as px


def linePixels(pin0, pin1):
    length = int(np.hypot(pin1[0] - pin0[0], pin1[1] - pin0[1]))
    x = np.linspace(pin0[0], pin1[0], length)
    y = np.linspace(pin0[1], pin1[1], length)
    return (x.astype(int) - 1, y.astype(int) - 1)


class Canvas:

    def __init__(self,
                 filename,
                 img_radius=1000,
                 numPins=300,
                 initPin=0,
                 lineWidth=10,
                 lineWeight=10,
                 minLoop=3,
                 palette=None,
                 numLinesPerColour=None,
                 group_orders=None
                 ):

        self.filename = filename
        self.img_radius = img_radius
        self.numPins = numPins
        self.initPin = initPin
        self.lineWidth = lineWidth
        self.lineWeight = lineWeight
        self.minLoop = minLoop

        self.totalLines = []
        self.Coords = self.pinCoords()

        self.base_img = Image.open(self.filename).resize((self.img_radius * 2 + 1, self.img_radius * 2 + 1))

        if palette is not None:

            assert set(palette.keys()) == set(numLinesPerColour.keys()), "Palette keys and numLinesPerColour keys don't match"
            self.palette = palette
            self.numLinesPerColour = numLinesPerColour
            self.colors_array = np.array(list(self.palette.values()))
            self.np_img = np.array(self.base_img, dtype=float)
            self.img_couleur_sep = dict()
            self.d_couleur_threaded = dict()

            self.color_names = list(self.palette.keys())
            self.color_values = list(self.palette.values())
            first_color_letters = [color[0] for color in self.color_names]
            assert len(set(first_color_letters)) == len(first_color_letters), "First letter of each color name must be unique."
            assert set(first_color_letters) == set(group_orders), "Invalid letter in group_order"
            self.group_orders = group_orders

            for keys in self.palette.keys():
                self.img_couleur_sep[keys] = np.zeros(self.np_img.shape[:2])

            # self.maskImage()
            self.img_dithered = self.fs_dither()

        else:
            self.np_img = np.array(self.base_img.convert('L'), dtype=float)
            self.invertImage()
            self.img_couleur_sep = dict(
                grey=self.np_img
            )
            # Image.fromarray(self.img).show()

    def pinCoords(self, offset=0, x0=None, y0=None):
        alpha = np.linspace(0 + offset, 2 * np.pi + offset, self.numPins + 1)

        if (x0 is None) or (y0 is None):
            x0 = self.img_radius + 1
            y0 = self.img_radius + 1

        coords = []
        for angle in alpha[0:-1]:
            x = int(x0 + self.img_radius * np.cos(angle))
            y = int(y0 + self.img_radius * np.sin(angle))

            coords.append((x, y))
        return coords

    def ComputeThreads(self, numLines, colour="grey") -> []:

        img = self.img_couleur_sep[colour]
        height, width = img.shape[0:2]

        # Initialize variables
        i = 0
        lines = []
        previousPins = []
        oldPin = self.initPin
        lineMask = Image.new("L", (width, height))
        lineMaskD = ImageDraw.Draw(lineMask)
        for line in range(numLines):
            i += 1
            bestLine = 0
            oldCoord = self.Coords[oldPin]

            # Loop over possible lines
            for index in range(1, self.numPins):
                pin = (oldPin + index) % self.numPins

                coord = self.Coords[pin]

                xLine, yLine = linePixels(oldCoord, coord)

                # Fitness function
                lineSum = np.sum(img[yLine, xLine])

                if (lineSum > bestLine) and not (pin in previousPins):
                    bestLine = lineSum
                    bestPin = pin

            # Update previous pins
            if len(previousPins) >= self.minLoop:
                previousPins.pop(0)
            previousPins.append(bestPin)

            # Subtract new line from image

            lineMask.paste(0, (0, 0, height, width))
            lineMaskD.line((oldCoord, self.Coords[bestPin]), self.lineWeight, self.lineWidth)
            img = np.subtract(img, lineMask)

            # Save line to results\
            if colour == "grey":
                lines.append((self.Coords[oldPin], self.Coords[bestPin], (0, 0, 0)))
            else:
                lines.append((self.Coords[oldPin], self.Coords[bestPin], self.palette[colour]))

            # Break if no lines possible
            if bestPin == oldPin:
                break

            # Prepare for next loop
            oldPin = bestPin

            # Print progress
            sys.stdout.write("\b\b")
            sys.stdout.write("\r")
            sys.stdout.write("[+] Computing line " + str(line + 1) + " of " + str(numLines) + " total")
            sys.stdout.flush()

        print("\n[+] Image threaded")

        return lines

    def buildCanvas(self, numLines=0):

        if self.palette is None:
            assert numLines != 0, "Must specify number of lines in buildCanvas, for Greyscale"
            self.totalLines = self.ComputeThreads(numLines, "grey")
            return self.totalLines

        else:
            for key in self.palette.keys():
                self.d_couleur_threaded[key] = self.ComputeThreads(self.numLinesPerColour[key], key)

            color_names = list(self.palette.keys())
            color_counters = {k: 0 for k in color_names}

            for g in self.group_orders:
                num_instances = len([c for c in self.group_orders if c == g])
                matching_color = [c for c in color_names if c[0] == g][0]
                color_value = self.palette[matching_color]
                color_counters[matching_color] += 1
                color_len = len(self.d_couleur_threaded[matching_color])
                start = int(color_len * (color_counters[matching_color] - 1) / num_instances)
                end = int(color_len * color_counters[matching_color] / num_instances)
                next_lines = self.d_couleur_threaded[matching_color][start: end]
                for line in next_lines:
                    self.totalLines.append(line)


    def paintCanvas(self):
        output = Image.new('RGB', (self.img_radius * 2, self.img_radius * 2), (255, 255, 255))
        outputDraw = ImageDraw.Draw(output)
        for line in self.totalLines:
            outputDraw.line((line[0], line[1]), line[2])
        output.show()
        return output

    def GetClosestPaletteColour(self, old_val):
        distances = np.sqrt(np.sum((self.colors_array - old_val) ** 2, axis=1))
        closest = np.where(distances == np.amin(distances))[0][0]
        colour = list(self.palette.keys())[closest]
        return colour

    def fs_dither(self):
        arr = self.np_img
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
            sys.stdout.write("[+] Dithering " + str(int(ir / height * 100)) + "% complete")
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
    #     imgSized = cv2.resize(imgCropped, (2 * img_radius + 1, 2 * img_radius + 1))
    #     return imgSized

    # Invert grayscale image
    def invertImage(self):
        self.np_img = 255 - self.np_img

    # Apply circular mask to image
    def maskImage(self):
        radius = self.img_radius
        y, x = np.ogrid[-radius:radius, -radius:radius]
        mask = x ** 2 + y ** 2 > radius ** 2
        self.np_img[mask] = 0

    def showDitheredImage(self):
        px.imshow(self.np_img, template="plotly_dark").show()
        fig = px.imshow(
            np.array(list(self.img_couleur_sep.values())), template="plotly_dark",
            title="Images per color", animation_frame=0, color_continuous_scale="gray"
        ).update_layout(coloraxis_showscale=False)
        fig.layout.sliders[0].currentvalue.prefix = "color = "
        for i, color_name in enumerate(self.palette.keys()):
            fig.layout.sliders[0].steps[i].label = color_name
        fig.show()
