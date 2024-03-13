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
        img_radius = 500,
        numPins=200,
        lineWidth=10,
        lineWeight=10,
        group_orders="worbworbworb"
    )
    # for r in range(250, 1251, 250):
    #     canvas = Canvas(**args,img_radius=r)
    #     # canvas.showDitheredImage()
    #     for c in range(100, 301, 50)
    canvas = Canvas(**args)
    for keys in canvas.img_couleur_sep.keys():
        im = Image.fromarray(np.uint8(canvas.img_couleur_sep[keys]))
        im.save("Threaded_%s.png"%keys)
    im = Image.fromarray(np.uint8(canvas.img_dithered))
    im.save("Threaded.png")

    canvas.buildCanvas()
    output = canvas.paintCanvas()
    output.save("tniggggaa.jpg")
    # WriteThreadedCsvFile("../outputs/tigga.csv", canvas.totalLines)
    # for keys in canvas.img_dithered.keys():
    #     im = Image.fromarray(canvas.img_dithered[keys],mode='L')
    #     im.save("Threaded_%s.png"%keys)