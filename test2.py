import numpy as np


a = np.arange(57)*10
idx = (np.abs(a - 555)).argmin()
print(idx)


