from PyQt5.QtWidgets import (QWidget, QSlider, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
import numpy as np
import tifffile as tf


def rebin_image(im,bin_factor):
    arrx,arry = np.shape(im)
    if arrx/bin_factor != int or arrx/bin_factor != int:
        print(arrx,arry)
        print('error')

    else:
        shape = (arrx/bin_factor,arry/bin_factor)
        return im.reshape(shape).mean(-1).mean(1)

img = tf.imread('Site4um.tiff')[-1]

r_im = rebin_image(img,2)
