import numpy as np
import sys
from PIL import Image, ImageDraw
from ColourSplit import *


def linePixels(pin0, pin1):
    length = int(np.hypot(pin1[0] - pin0[0], pin1[1] - pin0[1]))
    x = np.linspace(pin0[0], pin1[0], length)
    y = np.linspace(pin0[1], pin1[1], length)
    return (x.astype(int) - 1, y.astype(int) - 1)


class Canvas:

    def __init__(self, ImgRadius=500, numPins=300, lineWidth=3, lineWeight=80, minLoop=3):
        self.ImgRadius = ImgRadius
        self.numPins = numPins
        self.lineWidth = lineWidth
        self.lineWeight = lineWeight
        self.minLoop = minLoop

        self.Coords = self.pinCoords()

    def pinCoords(self, offset=0, x0=None, y0=None):
        alpha = np.linspace(0 + offset, 2 * np.pi + offset, self.numPins + 1)

        if (x0 is None) or (y0 is None):
            x0 = self.ImgRadius + 1
            y0 = self.ImgRadius + 1

        coords = []
        for angle in alpha[0:-1]:
            x = int(x0 + self.ImgRadius * np.cos(angle))
            y = int(y0 + self.ImgRadius * np.sin(angle))

            coords.append((x, y))
        return coords

    # Compute a line mask

    def ComputeThreads(self, I: Img, colour, numLines, initPin=0) -> []:
        # image result is rendered to
        img = I.img_couleur_sep[colour]
        height, width = img.shape[0:2]

        # Initialize variables
        i = 0
        lines = []
        previousPins = []
        oldPin = initPin
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

            lineMask.paste(0, (0,0,height,width))
            # xlineMask, ylineMask = linePixels(oldCoord, self.Coords[bestPin])
            lineMaskD.line((oldCoord,self.Coords[bestPin]), self.lineWeight, self.lineWidth)
            img = np.subtract(img,lineMask)


            # Save line to results
            lines.append((self.Coords[oldPin], self.Coords[bestPin], I.palette[colour]))

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
        # Wait for user and save before exit
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite('./threaded_%s.png'%colour, imgResult)

        return lines

    def paintCanvas(self, lines):
        output = Image.new('RGB',(self.ImgRadius*2,self.ImgRadius*2))
        outputDraw = ImageDraw.Draw(output)
        for line in lines:
            outputDraw.line((line[0], line[1]), line[2])
        output.show()