#!/usr/bin/env python
import numpy as np

from Canvas import *
from misc import *
import time

if __name__ == "__main__":

    args = dict(
        filename="John_Xina.png",
        palette=dict(
            noir=(0, 0, 0),
            white=(255, 255, 255),
            green=(30,45,45),
            beige=(80,60,55),
            dark_beige=(40,25,25),
            # piss_blue=(65,80,85)
        ),
        group_orders="wgbdn"*4,
        # TopLeftPixel=(0,250),
        # fillcolor=(65,80,85)

    )


    start = time.time()
    canvas = Canvas(**args,img_radius=1000, numPins=250, lineWidth=7)
    end = time.time()
    print("\n", end - start)
    canvas.showDitheredImage()
    canvas.buildCanvas(background=(65,80,85),excludeBackground=True)
    output = canvas.paintCanvas(background=(65,80,85)).astype(np.float32)
    output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    cv2.imshow('bal', output)
    cv2.waitKey(0)
    cv2.imwrite("xina.png", output)

    # for i in range(300,301,100):
    # canvas.pinCoords(i)
    # canvas.buildCanvas()
    # output = canvas.paintCanvas((0, 0, 0))
    # output.save("kobe_%i.png" % i)
