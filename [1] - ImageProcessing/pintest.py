#!/usr/bin/env python

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Canvas import *
from misc import *

if __name__ == "__main__":
    list_of_waltuh = []
    for i in range(100, 301, 25):
        # canvas = Canvas("waltuhIRL.jpg", numPins=i)
        # lines = canvas.ComputeThreads(6000)
        # output = canvas.paintCanvas(lines)
        # output.save("waltuh_%i.png" % i)
        next_waltuh_path = "waltuh_%i.png"%i
        next_waltuh = np.array(Image.open(next_waltuh_path), dtype=float)
        list_of_waltuh.append(next_waltuh)

    fig = px.imshow(
        np.array(list_of_waltuh), template="plotly_dark",
        title="images per pins", animation_frame=0, color_continuous_scale="gray"
    ).update_layout(coloraxis_showscale=False)
    fig.layout.sliders[0].currentvalue.prefix = "number of pins = "
    for i, numpins in enumerate([100, 125, 150, 175, 200, 225, 250, 275, 300]):
        fig.layout.sliders[0].steps[i].label = numpins
    fig.show()
