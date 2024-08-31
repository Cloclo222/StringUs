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
# import pyi_splash


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    # pyi_splash.close()
    sys.exit(app.exec_())

