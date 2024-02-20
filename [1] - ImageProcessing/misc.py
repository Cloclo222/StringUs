import itertools

from Canvas import *
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2


def centerImg(filename, fillColor=(255, 255, 255), Topleftpixel=(0, 0), imgDiameter=1000):
    img = Image.open(filename)
    img = np.array(img)

    img_cropped = (np.ones((imgDiameter, imgDiameter, 3)) * fillColor)

    # source img ================================================================================================================================

    rowStart = Topleftpixel[0] if Topleftpixel[0] >= 0 else 0
    colomnStart = Topleftpixel[1] if Topleftpixel[1] >= 0 else 0
    rowEnd = img.shape[0] if (imgDiameter + Topleftpixel[0]) > img.shape[0] else (imgDiameter + Topleftpixel[0])
    colomnEnd = img.shape[1] if (imgDiameter + Topleftpixel[1]) > img.shape[1] else (imgDiameter + Topleftpixel[1])

    # cropped img =========================================================================================================================================

    rowStartCropped = np.abs(Topleftpixel[0]) if not Topleftpixel[0] >= 0 else 0
    colomnStartCropped = np.abs(Topleftpixel[1]) if not Topleftpixel[1] >= 0 else 0


    rowEndcropped = imgDiameter if imgDiameter< img.shape[0] - Topleftpixel[0] else img.shape[0] -Topleftpixel[0]


    colomnEndcropped = imgDiameter if imgDiameter< img.shape[1] - Topleftpixel[1] else img.shape[1] - Topleftpixel[1]

    img_cropped[rowStartCropped:rowEndcropped, colomnStartCropped:colomnEndcropped] = img[rowStart:rowEnd,
                                                                                      colomnStart:colomnEnd]

    return img_cropped.astype(np.uint8)


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


def createGrid(folder=None):
    # User defined variables
    dirname = "imgs/tiger_ratio"  # Name of the directory containing the images
    name = "outputs/tiger_grid" + ".jpg"  # Name of the exported file
    margin = 20  # Margin between pictures in pixels
    w = 5  # Width of the matrix (nb of images)
    h = 5  # Height of the matrix (nb of images)
    n = w * h

    filename_list = []

    for file in os.listdir(dirname):
        # if file.endswith(".JPG"):
        filename_list.append(file)

    filename_list.sort();

    print(filename_list)

    imgs = [cv2.resize(cv2.imread(os.getcwd() + "/" + dirname + "/" + file), (1000, 1000), interpolation=cv2.INTER_AREA)
            for file in filename_list]

    # Define the shape of the image to be replicated (all images should have the same shape)
    img_h, img_w, img_c = imgs[0].shape

    # Define the margins in x and y directions
    m_x = margin
    m_y = margin

    # Size of the full size image
    mat_x = img_w * w + m_x * (w - 1)
    mat_y = img_h * h + m_y * (h - 1)

    # Create a matrix of zeros of the right size and fill with 255 (so margins end up white)
    imgmatrix = np.ones((mat_y, mat_x, img_c), np.uint8) * 255

    # Prepare an iterable with the right dimensions
    positions = itertools.product(range(h), range(w))

    for (y_i, x_i), img in zip(positions, imgs):
        x = x_i * (img_w + m_x)
        y = y_i * (img_h + m_y)
        imgmatrix[y:y + img_h, x:x + img_w, :] = img

    resized = cv2.resize(imgmatrix, (mat_x, mat_y), interpolation=cv2.INTER_AREA)
    compression_params = [cv2.IMWRITE_JPEG_QUALITY, 90]
    cv2.imwrite(name, resized, compression_params)


if __name__ == "__main__":
    filep = 'imgs/the_rock.jpg'
    img = centerImg(filep, Topleftpixel=(1000, 1000), imgDiameter= 1000)
    New_img = Image.fromarray(img)
    New_img.show()
    cv2.waitKey(0)
