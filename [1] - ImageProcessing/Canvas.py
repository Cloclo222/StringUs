import numpy as np
import sys
from PIL import Image, ImageDraw, ImageFilter
import plotly.express as px
import numba
import cv2


# @numba.guvectorize([(numba.int64[:,:], numba.int64[:], numba.int64[:], numba.float64[:])], '(n,n),(m),(m)->()')
@numba.njit
def LineSum(img, x, y):
    acc = 0
    for i, j in zip(x, y):
        acc += img[j, i]
    return acc


@numba.njit
def linePixels(pin0, pin1):
    length = int(np.hypot(pin1[0] - pin0[0], pin1[1] - pin0[1]))
    x = np.linspace(pin0[0], pin1[0], length)
    y = np.linspace(pin0[1], pin1[1], length)
    x = np.array([int(x[i]) for i in range(len(x))]) - 1
    y = np.array([int(y[i]) for i in range(len(y))]) - 1
    return x, y


@numba.njit
def ditherImg(arr, colors_array):
    arr_shape = np.shape(arr)
    num_imgs = len(colors_array)
    res_shape = num_imgs, arr_shape[0], arr_shape[1]
    res_dithered = np.zeros(arr_shape)
    result_sep = np.zeros(res_shape)
    height, width = arr.shape[0:2]
    for ir in range(height):
        for ic in range(width):
            old_val = arr[ir, ic].copy()
            distances = np.sqrt(np.sum((colors_array - old_val) ** 2, axis=1))
            closest = np.where(distances == np.amin(distances))[0][0]
            new_val = colors_array[closest]
            result_sep[closest, ir, ic] = 255
            res_dithered[ir, ic] = new_val
            err = old_val - new_val

            if ic < width - 1:
                arr[ir, ic + 1] += err * 3 / 16
            if ir < height - 1:
                if ic > 0:
                    arr[ir + 1, ic - 1] += err * 3 / 16
                arr[ir + 1, ic] += err * 5 / 16
                if ic < width - 1:
                    arr[ir + 1, ic + 1] += err / 16

        # sys.stdout.write("\b\b")
        # sys.stdout.write("\r")
        # sys.stdout.write("[+] Dithering " + str(int(ir / height * 100)) + "% complete")
        # sys.stdout.flush()
    return [res_dithered, result_sep]


def ComputeThreads(img, numLines, numPins, Coords, initPin=0, minLoop=3, lineWeight=10, lineWidth=10,
                   colour=(0, 0, 0)) -> []:
    height, width = img.shape[0:2]

    # Initialize variables
    i = 0
    lines = []
    previousPins = []
    oldPin = initPin
    lineMask = np.zeros_like(img)
    # lineMask = Image.new("L", (width, height))
    # lineMaskD = ImageDraw.Draw(lineMask)

    for line in range(numLines):
        i += 1
        bestLine = 0
        oldCoord = Coords[oldPin]

        # Loop over possible lines
        for index in range(1, numPins):
            pin = (oldPin + index) % numPins
            lineSum = 0
            coord = Coords[pin]

            xLine, yLine = linePixels(oldCoord, coord)
            # length = int(np.hypot(coord[0] - oldCoord[0], coord[1] - oldCoord[1]))
            # xLine = np.linspace(oldCoord[0], coord[0], length)
            # yLine = np.linspace(oldCoord[1], coord[1], length)
            # xLineint = np.array([int(xLine[i]) for i in range(len(xLine))]) - 1
            # yLineint = np.array([int(yLine[i]) for i in range(len(yLine))]) - 1
            # xarrange= np.arange(oldCoord[0], coord[0])
            # yarrange= np.arange(oldCoord[1], coord[1])

            # Fitness function
            # for y, x in zip(yLine, xLine):
            #     lineSum += img[y, x]
            Sum = LineSum(img, xLine, yLine)
            # Sum = np.sum(img[yLine, xLine])

            if (Sum > bestLine) and not (pin in previousPins):
                bestLine = Sum
                bestPin = pin

        # Update previous pins
        if len(previousPins) >= minLoop:
            previousPins.pop(0)
        previousPins.append(bestPin)

        # Subtract new line from image

        # xMask, yMask = linePixels(oldCoord, Coords[bestPin])
        lineMask = lineMask * 0
        # img = LineMask(img, xMask, yMask, lineWeight)

        cv2.line(lineMask, oldCoord, Coords[bestPin], lineWeight, lineWidth)
        img = np.subtract(img, lineMask)

        # lineMask.paste(0, (0, 0, height, width))
        # lineMaskD.line((oldCoord, Coords[bestPin]), lineWeight, lineWidth)
        # img = np.subtract(img, lineMask)

        kobe = img / 255
        cv2.imshow('kobe', cv2.resize(kobe, (1000, 1000)))
        cv2.waitKey(10)

        # Save line to results\

        lines.append((Coords[oldPin], Coords[bestPin], colour))

        # Break if no lines possible
        if bestPin == oldPin:
            break

        # Prepare for next loop
        oldPin = bestPin

        # Print progress
        # sys.stdout.write("\b\b")
        # sys.stdout.write("\r")
        # sys.stdout.write("[+] Computing " + colour + " line " + str(line + 1) + " of " + str(numLines) + " max")
        # sys.stdout.flush()

    return lines


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
                 group_orders=None,
                 ):

        self.numLinesPerColour = numLinesPerColour
        self.filename = filename
        self.img_radius = img_radius
        self.numPins = numPins
        self.initPin = initPin
        self.lineWidth = lineWidth
        self.lineWeight = lineWeight
        self.minLoop = minLoop
        self.Coords = None
        self.img_dithered = None

        self.totalLines = []

        self.base_img = Image.open(self.filename).resize((self.img_radius * 2 + 1, self.img_radius * 2 + 1))
        self.pinCoords()

        if palette is not None:
            if numLinesPerColour is None:
                self.numLinesPerColour = dict()
                for key in palette.keys():
                    self.numLinesPerColour[key] = 100000
            else:
                assert set(palette.keys()) == set(
                    numLinesPerColour.keys()), "Palette keys and numLinesPerColour keys don't match"
            self.palette = palette
            self.colors_array = np.array(list(self.palette.values()))
            self.np_img = np.array(self.base_img, dtype=float)
            self.img_couleur_sep = dict()
            self.d_couleur_threaded = dict()

            self.color_names = list(self.palette.keys())
            self.color_values = list(self.palette.values())
            first_color_letters = [color[0] for color in self.color_names]
            assert len(set(first_color_letters)) == len(
                first_color_letters), "First letter of each color name must be unique."
            # assert set(first_color_letters) == set(group_orders), "Invalid letter in group_order"
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
            # Image.fromarray(self.img).show()

    def pinCoords(self, numPins=300, offset=0, x0=None, y0=None):
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

    def buildCanvas(self, numLines=10000, background=(255, 255, 255), excludeBackground=False):

        if self.palette is None:
            # assert numLines != 0, "Must specify number of lines in buildCanvas, for Greyscale"
            self.totalLines = ComputeThreads(self.img_couleur_sep["grey"],
                                             numLines=numLines,
                                             numPins=self.numPins,
                                             Coords=self.Coords,
                                             initPin=self.initPin,
                                             lineWidth=self.lineWidth,
                                             lineWeight=self.lineWeight,
                                             colour=(0, 0, 0))
            np.flip(self.totalLines)
            print("\n[+] Image threaded")
            return self.totalLines

        else:

            for key in self.palette.keys():
                if self.palette[key] == background and excludeBackground is True:
                    continue
                else:
                    self.d_couleur_threaded[key] = ComputeThreads(self.img_couleur_sep[key],
                                                                  numLines=self.numLinesPerColour[key],
                                                                  numPins=self.numPins,
                                                                  Coords=self.Coords,
                                                                  initPin=self.initPin,
                                                                  lineWidth=self.lineWidth,
                                                                  lineWeight=self.lineWeight,
                                                                  colour=self.palette[key])
                    print("Threaded %i %s lines" % (len(self.d_couleur_threaded[key]), key))

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
            print("[+] Image threaded\n")

    def paintCanvas(self, background=(255, 255, 255)):
        output = np.ones((self.img_radius*2, self.img_radius*2,3))*background
        # output = Image.new('RGB', (self.img_radius * 2, self.img_radius * 2), background)
        # outputDraw = ImageDraw.Draw(output)
        for line in self.totalLines:
            cv2.line(output, line[0], line[1], line[2])
            # outputDraw.line((line[0], line[1]), fill=line[2], width=self.lineWidth)
        # output.show()
        return output

    def fs_dither(self):
        res = ditherImg(self.np_img, self.colors_array)
        self.img_dithered = np.array(res[0])
        for i, key in enumerate(self.palette.keys()):
            img_blur = cv2.blur(res[1][i], (3, 3))
            # cv2.imshow('nig', img_blur/255)
            # cv2.waitKey(0)
            self.img_couleur_sep[key] = img_blur
            # self.img_couleur_sep[key] = res[1][i]

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
        px.imshow(self.img_dithered, template="plotly_dark").show()
        fig = px.imshow(
            np.array(list(self.img_couleur_sep.values())), template="plotly_dark",
            title="Images per color", animation_frame=0, color_continuous_scale="gray"
        ).update_layout(coloraxis_showscale=False)
        fig.layout.sliders[0].currentvalue.prefix = "color = "
        for i, color_name in enumerate(self.palette.keys()):
            fig.layout.sliders[0].steps[i].label = color_name
        fig.show()
