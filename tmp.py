import os
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns
#os.chdir('D:/Practical Time Series/')
zero_mean_series = np.random.normal(loc=0.0, scale=1., size=100)
plt.plot(zero_mean_series)
plt.show()