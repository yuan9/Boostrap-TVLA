import matplotlib.pyplot as plt
import sys
import numpy as np
import scipy.stats

bootnum=1000
bin_num = 100

step =  float(1)/bootnum
_c = []
value = 0
for i in range(0,bootnum):
	_c.append(value)
	value = value + step
c = np.array(_c)
#c = np.random.uniform(0,1,1000)


bin_width = (np.amax(c) - np.amin(c))/bin_num
bins_array = np.arange(np.amin(c),np.amax(c)+bin_width,bin_width)

plt.hist(c, bins=bins_array, edgecolor='black', linewidth=0.5)

plt.ylim(0,12)
plt.show()
