import numpy as np
import matplotlib.pyplot as plt
from Canvas import *

def animate(lines, coords, imgRadius):
    # plot results
    imgResult = np.ones((imgRadius * 2, imgRadius * 2, 3)) * 125
    for l in lines:
        xLine, yLine = linePixels(coords[l[0]], coords[l[1]])
        imgResult[yLine, xLine] = l[2]
        cv2.imshow('image', imgResult)
        cv2.waitKey(1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def WriteThreadedFile(mode: str, colour, lines, coords, imgRadius):
    mode = mode.lower()
    match mode:
        case "csv":
            csv_output = open('threaded_%s.csv' % colour, 'wb')
            csv_output.write("x1,y1,x2,y2\n".encode('utf8'))
            csver = lambda c1, c2: "%i,%i" % c1 + "," + "%i,%i" % c2 + "\n"
            for l in lines:
                csv_output.write(csver(coords[l[0]], coords[l[1]]).encode('utf8'))
            csv_output.close()

        case "svg":
            svg_output = open('threaded_%s.svg' % colour, 'wb')
            header = """<?xml version="1.0" standalone="no"?>
                <svg width="%i" height="%i" version="1.1" xmlns="http://www.w3.org/2000/svg">
                """ % (imgRadius * 2, imgRadius * 2)
            footer = "</svg>"
            svg_output.write(header.encode('utf8'))
            pather = lambda d: '<path d="%s" stroke="black" stroke-width="0.5" fill="none" />\n' % d
            pathstrings = []
            pathstrings.append("M" + "%i %i" % coords[lines[0][0]] + " ")
            for l in lines:
                nn = coords[l[1]]
                pathstrings.append("L" + "%i %i" % nn + " ")
            pathstrings.append("Z")
            d = "".join(pathstrings)
            svg_output.write(pather(d).encode('utf8'))
            svg_output.write(footer.encode('utf8'))
            svg_output.close()