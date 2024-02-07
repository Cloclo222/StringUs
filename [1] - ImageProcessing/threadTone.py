#!/usr/bin/env python

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ColourSplit import *
from Canvas import *
from misc import *

# Parameters
imgRadius = 250  # Number of pixels that the image radius is resized to

initPin = 0  # Initial pin to start threading from
numPins = 300  # Number of pins on the circular loom

Greyscale = False  # choose to greyscale image or not

minLoop = 3  # Disallow loops of less than minLoop lines
lineWidth = 1  # The number of pixels that represents the width of a thread
lineWeight = 20  # The weight a single thread has in terms of "darkness"

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


if __name__ == "__main__":

    palette = dict()
    palette['white'] = (255, 255, 255)
    palette['black'] = (0, 0, 0)
    palette['red'] = (220, 0, 0)
    palette['orange'] = (255, 130, 0)


    image = Img(imgPath, palette)
    # image = Img(imgPath)
    # image.showImage()
    # canvas = Canvas(image.img_radius)
    # lines = canvas.ComputeThreads(image, 6000)
    # output = canvas.paintCanvas(lines)
    # output.save("output.png")


