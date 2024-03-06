#!/usr/bin/env python
import cv2
import numpy as np

from Canvas import *
from misc import *
import time

if __name__ == "__main__":
    args = dict(
        filename="shronk.png",
        palette=dict(
            noir=(0, 0, 0),
            white=(255, 255, 255),
            green=(159, 169, 59),
            dark_green=(91,90,45),
            pink=(157, 69, 115),
            shit_brown=(107, 60, 46),
            blue=(54,68,134)
        ),
        group_orders="wsgdpbn"*5
    )
    start = time.time()
    canvas = Canvas(**args, img_radius=1000, numPins=300, lineWidth=7, Cropping=True, Topleftpixel=(0,250), CropDiameter=550)
    # canvas.showDitheredImage()
    end = time.time()
    print("image dithered in %.3fs" % (end - start))
    start = time.time()
    canvas.buildCanvas()
    end = time.time()
    print("Image threaded in %.3f"%(end - start))
    output = canvas.paintCanvas((0, 0, 0))
    output.show()
    # output.save("kobe_test.png")
    WriteThreadedCsvFile("../outputs/shronk.csv", canvas.totalLines)
