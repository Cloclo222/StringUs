import multiprocessing
import sys
import cv2
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Window.Main_Window import *
import pandas as pd
from PIL import ImageDraw
# import plotly.express as px
import imageio.v2
import cv2
import numba
import glob
try:
    import pyi_splash
except:
    pass


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        pyi_splash.close()
    except:
        pass

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
