#!/usr/bin/env python
import cv2
import numpy as np

from Canvas import *
from misc import *
import time

if __name__ == "__main__":
    args = dict(
        filename="the_rock.jpg",
        palette=dict(
            noir=(0, 0, 0),
            white=(255, 255, 255),
            purple=(34, 15, 79),
            yellow=(225, 180, 0),
            brown=(121, 69, 11)
        ),
        group_orders="wybpwybpwybpn"
    )
    start = time.time()
    canvas = Canvas(**args, img_radius=1000, numPins=250, lineWidth=7)
    canvas.paintCanvas()
    end = time.time()
    print("image dithered in %.3fs" % (end - start))
    # canvas.showDitheredImage()
    # for i in range(300,301,100):
    # canvas.pinCoords(i)
    start = time.time()
    canvas.buildCanvas(excludeBackground=False, background=(0, 0, 0))
    end = time.time()
    print("Image threaded in %.3f"%(end - start))
    output = canvas.paintCanvas((0, 0, 0)).astype(np.float32)
    output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    cv2.imshow('bal',output)
    cv2.waitKey(0)
    cv2.imwrite("kobe_test.png", output)
    # output.show()
    # output.save("kobe_test.png")
