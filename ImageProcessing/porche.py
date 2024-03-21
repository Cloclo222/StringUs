#!/usr/bin/env python

from Canvas import *
from misc import *

if __name__ == "__main__":
    args = dict(
        filename="imgs/porche.png",
        palette=dict(
            white=(255, 255, 255),
            black=(0, 0, 0),
            red=(220, 0, 0),
            gray=(125, 125, 125)
        ),
        numLinesPerColour=dict(
            white=4000,
            black=4000,
            red=2000,
            gray=4000
        ),
        group_orders="wgrbwgrbwgrb"
    )

    canvas = Canvas(**args)
    canvas.showDitheredImage()
    canvas.buildCanvas()
    output = canvas.paintCanvas()
    output.save("output_porche.png")
