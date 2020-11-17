import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.optimize as opt
import sklearn.decomposition as sd
import sklearn.cluster as sc
import matplotlib.pyplot as plt
import h5py
import tifffile as tf
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

from scipy.signal import savgol_filter
import sys
import pyqtgraph as pg


img = tf.imread('test_stack.tiff')
# -*- coding: utf-8 -*-


img1 = img[10].flatten()
img2 = img[20].flatten()
img3 = img[30].flatten()

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
g = gl.GLGridItem()
w.addItem(g)

#generate random points from -10 to 10, z-axis positive
pos = np.array((img1,img2)).T
pos[:,2] = np.abs(pos[:,2])

sp2 = gl.GLScatterPlotItem(pos=pos)
w.addItem(sp2)

#generate a color opacity gradient
color = np.zeros((pos.shape[0],4), dtype=np.float32)
color[:,0] = 1
color[:,1] = 0
color[:,2] = 0.5
color[0:100,3] = np.arange(0,100)/100.

def update():
    ## update volume colors
    global color
    color = np.roll(color,1, axis=0)
    sp2.setData(color=color)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)


if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()