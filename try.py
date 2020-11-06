import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy.optimize as opt
import sklearn.decomposition as sd
import sklearn.cluster as sc
import matplotlib.pyplot as plt
import h5py
import tifffile as tf

from scipy.signal import savgol_filter


img = tf.imread(r'C:\Users\pattammattel\Desktop\Spectromicroscopy\HXN_Data\amap_site4um.tiff')

#print(img.shape)
