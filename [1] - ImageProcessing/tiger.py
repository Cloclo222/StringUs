#!/usr/bin/env python

from Canvas import *
from misc import *

if __name__ == "__main__":
    args = dict(
        filename="tiger/tiger.jpg",
        palette=dict(
            white=(255, 255, 255),
            black=(0, 0, 0),
            red=(220, 0, 0),
            orange=(255, 130, 0)
        ),
        group_orders="worbworbworb"
    )
    # for r in range(250, 1251, 250):
    #     canvas = Canvas(**args,img_radius=r)
    #     # canvas.showDitheredImage()
    #     for c in range(100, 301, 50)
    canvas = Canvas(**args,img_radius = 1000)
    canvas.pinCoords(300)
    canvas.buildCanvas()
    output = canvas.paintCanvas()
    ratio = float(2*np.pi/300)
    output.save("tiger_ratio/tiger_r%i_c%i_ratio%.3f.jpg"%(1000,300,ratio))
    WriteThreadedCsvFile("../outputs/tigga.csv", canvas.totalLines)
