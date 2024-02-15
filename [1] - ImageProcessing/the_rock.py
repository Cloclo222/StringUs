#!/usr/bin/env python

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
        group_orders="wypbnwypbnwypbn"
    )

    start = time.time()
    canvas = Canvas(**args,img_radius=1000)
    end = time.time()
    print("\n", end - start)
    canvas.showDitheredImage()
    # for i in range(300,301,100):
    # canvas.pinCoords(i)
    # canvas.buildCanvas()
    # output = canvas.paintCanvas((0, 0, 0))
    # output.save("kobe_%i.png" % i)
