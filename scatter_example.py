# -*- coding: utf-8 -*-
"""
Demonstration of ScatterPlotWidget for exploring structure in tabular data.

The widget consists of four components:

1) A list of column names from which the user may select 1 or 2 columns
    to plot. If one column is selected, the data for that column will be
    plotted in a histogram-like manner by using pg.pseudoScatter().
    If two columns are selected, then the
    scatter plot will be generated with x determined by the first column
    that was selected and y by the second.
2) A DataFilter that allows the user to select a subset of the data by
    specifying multiple selection criteria.
3) A ColorMap that allows the user to determine how points are colored by
    specifying multiple criteria.
4) A PlotWidget for displaying the data.

"""
#import initExample  ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle('pyqtgraph example: ScatterPlot')

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
