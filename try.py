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
