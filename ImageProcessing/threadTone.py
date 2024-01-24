#!/usr/bin/env python

import sys
import cv2
import numpy as np
from Pylette import extract_colors
from colorthief import ColorThief

# Parameters
imgRadius = 250  # Number of pixels that the image radius is resized to

initPin = 0  # Initial pin to start threading from
numPins = 1000  # Number of pins on the circular loom
numLines = 4000  # Maximal number of lines
Greyscale = False  # choose to greyscale image or not

minLoop = 3  # Disallow loops of less than minLoop lines
lineWidth = 5  # The number of pixels that represents the width of a thread
lineWeight = 15  # The weight a single thread has in terms of "darkness"

helpMessage = """
To use this tool, run:
python threadTone.py -p image-path -l number-of-lines-to-draw -n number-of-pins-to-draw-with

ex: python threadTone.py -p kitten.jpg -l 2000 -n 250
ex: python threadTone.py -p puppr.png

Note: imgPath is a required field.
"""
args = sys.argv

# \/argument interpreter
for arg in args:
    if arg == "-h" or arg == "-?" or arg == "help":
        print(helpMessage)
        sys.exit()

argNum = 1
while argNum < len(args):
    if args[argNum][0] == "-":
        flag = args[argNum]
        if flag == "-p" or flag == "-P":
            imgPath = args[argNum + 1]
            argNum += 2
        elif flag == "-l" or flag == "-L":
            try:
                int(args[argNum + 1])
            except ValueError:
                print("'" + args[
                    argNum + 1] + "' is not an integer, please input an integer for the number of lines to draw.")
                sys.exit(1)
            numLines = int(args[argNum + 1])
            argNum += 2
        elif flag == "-n" or flag == "-N":
            try:
                int(args[argNum + 1])
            except ValueError:
                print("'" + args[argNum + 1] + "' is not an integer, please input an integer for the number of pins.")
                sys.exit(1)
            numPins = int(args[argNum + 1])
            argNum += 2
        elif flag == "-gs" or flag == "-GS":
            Greyscale = args[argNum + 1]
            argNum += 2
        else:
            print("Invalid flag: " + args[argNum])
            sys.exit(1)
    else:
        print("Invalid flag: " + args[argNum])
        sys.exit(1)


# Invert grayscale image
def invertImage(image):
    return (255 - image)


# Apply circular mask to image
def maskImage(image, radius):
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
    mask = x ** 2 + y ** 2 > radius ** 2
    image[mask] = 0

    return image


# Compute coordinates of loom pins
def pinCoords(radius, numPins=200, offset=0, x0=None, y0=None):
    alpha = np.linspace(0 + offset, 2 * np.pi + offset, numPins + 1)

    if (x0 is None) or (y0 is None):
        x0 = radius + 1
        y0 = radius + 1

    coords = []
    for angle in alpha[0:-1]:
        x = int(x0 + radius * np.cos(angle))
        y = int(y0 + radius * np.sin(angle))

        coords.append((x, y))
    return coords


# Compute a line mask
def linePixels(pin0, pin1):
    length = int(np.hypot(pin1[0] - pin0[0], pin1[1] - pin0[1]))

    x = np.linspace(pin0[0], pin1[0], length)
    y = np.linspace(pin0[1], pin1[1], length)

    return x.astype(int) - 1, y.astype(int) - 1


def imagePreProcessing(image):
    #  Crop image
    height, width = image.shape[0:2]
    minEdge = min(height, width)
    topEdge = int((height - minEdge) / 2)
    leftEdge = int((width - minEdge) / 2)
    imgCropped = image[topEdge:topEdge + minEdge, leftEdge:leftEdge + minEdge]
    # cv2.imwrite('./cropped.png', imgCropped)

    # Resize image
    imgSized = cv2.resize(imgCropped, (2 * imgRadius + 1, 2 * imgRadius + 1))
    return imgSized


def GetClosestPaletteColour(old_val, palette):
    colours = list(palette.values())
    distances = np.sqrt(np.sum((colours-old_val)**2, axis=1))
    closest = np.where(distances == np.amin(distances))[0][0]
    colour = list(palette.keys())[list(palette.values()).index(colours[closest])]
    return colour


def fs_dither(img, palette: []):
    arr = np.array(img, dtype=float)
    height, width = arr.shape[0:2]
    for ir in range(height):
        for ic in range(width):
            old_val = arr[ir, ic].copy()
            new_colour = GetClosestPaletteColour(old_val, palette)
            new_val = palette[new_colour]
            img_couleur_sep[new_colour][ir][ic] = [0,0,0]
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


    # carr = np.array(arr / np.max(arr, axis=(0, 1)) * 255, dtype=np.uint8)
    return arr


def ComputeThreads(img, coords, colour='grey'):
    # image result is rendered to
    height, width = img.shape[0:2]
    imgResult = 255 * np.ones((height, width))

    # Initialize variables
    i = 0
    lines = []
    previousPins = []
    oldPin = initPin
    lineMask = np.zeros((height, width))
    for line in range(numLines):
        i += 1
        bestLine = 0
        oldCoord = coords[oldPin]

        # Loop over possible lines
        for index in range(1, numPins):
            pin = (oldPin + index) % numPins

            coord = coords[pin]

            xLine, yLine = linePixels(oldCoord, coord)

            # Fitness function
            lineSum = np.sum(img[yLine, xLine])

            if (lineSum > bestLine) and not (pin in previousPins):
                bestLine = lineSum
                bestPin = pin

        # Update previous pins
        if len(previousPins) >= minLoop:
            previousPins.pop(0)
        previousPins.append(bestPin)

        # Subtract new line from image
        lineMask = lineMask * 0
        cv2.line(lineMask, oldCoord, coords[bestPin], lineWeight, lineWidth)
        img = np.subtract(img, lineMask)

        # Save line to results
        lines.append((oldPin, bestPin))

        # plot results
        xLine, yLine = linePixels(coords[bestPin], coord)
        imgResult[yLine, xLine] = 0
        cv2.imshow('image', imgResult)
        cv2.waitKey(1)

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
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # cv2.imwrite('./threaded_%s.png'%colour, imgResult)

    svg_output = open('threaded_%s.svg' % colour, 'wb')
    header = """<?xml version="1.0" standalone="no"?>
        <svg width="%i" height="%i" version="1.1" xmlns="http://www.w3.org/2000/svg">
        """ % (width, height)
    footer = "</svg>"
    svg_output.write(header.encode('utf8'))
    pather = lambda d: '<path d="%s" stroke="black" stroke-width="0.5" fill="none" />\n' % d
    pathstrings = []
    pathstrings.append("M" + "%i %i" % coords[lines[0][0]] + " ")
    for l in lines:
        nn = coords[l[1]]
        pathstrings.append("L" + "%i %i" % nn + " ")
    pathstrings.append("Z")
    d = "".join(pathstrings)
    svg_output.write(pather(d).encode('utf8'))
    svg_output.write(footer.encode('utf8'))
    svg_output.close()

    csv_output = open('threaded_%s.csv' % colour, 'wb')
    csv_output.write("x1,y1,x2,y2\n".encode('utf8'))
    csver = lambda c1, c2: "%i,%i" % c1 + "," + "%i,%i" % c2 + "\n"
    for l in lines:
        csv_output.write(csver(coords[l[0]], coords[l[1]]).encode('utf8'))
    csv_output.close()


if __name__ == "__main__":

    # Load image
    image = cv2.imread(imgPath)
    print("[+] loaded " + imgPath + " for threading..")

    # Define pin coordinates
    coords = pinCoords(imgRadius, numPins)

    # Crop image
    imgCropped = imagePreProcessing(image)
    cv2.imwrite('./Cropped.png', imgCropped)

    if Greyscale:
        # Convert to grayscale
        imgGray = cv2.cvtColor(imgCropped, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('./gray.png', imgGray)
        # Invert image
        imgInverted = invertImage(imgGray)
        # cv2.imwrite('./inverted.png', imgInverted)
        # Mask image
        imgMasked = maskImage(imgInverted, imgRadius)
        # cv2.imwrite('./masked.png', imgMasked)
        print("[+] image preprocessed for threading..")
        ComputeThreads(imgMasked, coords)
    else:
        # Mask image
        # colorthief = ColorThief(imgPath)
        # palette = extract_colors(imgPath,palette_size=10)
        # palette.display(save_to_file=False)
        # colours = [colour.rgb for colour in palette]

        palette = {}
        palette['white'] = (255, 255, 255)
        palette['red'] = (0,0,255)
        palette['orange'] = (0,130,255)
        palette['black'] = (0,0,0)
        img_couleur_sep = {}
        for keys in palette.keys():
            img_couleur_sep[keys] = np.ones_like(imgCropped)*255


        # colours = [(0,130,255), (0,0,255), (255,255,255),(0,0,0)]
        imgDithered = fs_dither(imgCropped, palette)
        maskImage(imgDithered, imgRadius)
        cv2.imwrite('./gayfag.png', imgDithered)
        print("[+] image preprocessed for threading..")
        for keys in img_couleur_sep.keys():
            cv2.imwrite('./Seperated_%s.png'%keys, img_couleur_sep[keys])




