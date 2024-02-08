#!/usr/bin/env python

from Canvas import *
from misc import *

if __name__ == "__main__":
    args = dict(
        filename="tiger.jpg",
        palette=dict(
            white=(255, 255, 255),
            black=(0, 0, 0),
            red=(220, 0, 0),
            orange=(255, 130, 0)
        ),
        numLinesPerColour=dict(
            white=4000,
            black=4000,
            red=2000,
            orange=4000
        ),
        group_orders="worbworbworb"
    )

    canvas = Canvas(**args)
    canvas.showDitheredImage()
    canvas.buildCanvas()
    output = canvas.paintCanvas()
    output.save("output.png")
