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

img1 = img[10].flatten()
img2 = img[50].flatten()

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('pyqtgraph example: ScatterPlot')

## create four areas to add plots
w1 = view.addPlot()

## There are a few different ways we can draw scatter plots; each is optimized for different types of data:


## 1) All spots identical and transform-invariant (top-left plot).
## In this case we can get a huge performance boost by pre-rendering the spot
## image and just drawing that image repeatedly.


s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 0, 120))
pos = np.array((img1,img2))
s1.setData(spots)
w1.addItem(s1)

print(np.shape(spots))

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
