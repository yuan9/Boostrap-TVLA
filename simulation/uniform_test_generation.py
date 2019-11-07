import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from scipy import stats
from scipy.stats import chi2
import random
import array
import os
import time
import sys
import decimal

a=sys.argv

bootnum = 1000
bin_num = 100
c = np.random.uniform(0,1,bootnum)
np.savetxt('uniform.txt',c,fmt = '%f', delimiter=',')
#print(c)
#def split(arr, size):
#    arrs = []
#    while len(arr) > size:
#      pice = arr[:size]
#      arrs.append(pice)
#      arr = arr[size:]
#    arrs.append(arr)
#    return arrs
#c_array = split(c,1)
c_array = c[:,np.newaxis].tolist()
#print (c_array)

target_list = c
#min = np.amin(target_list)
#max = np.amax(target_list)
min = 0
max =1
print("{}-{}".format(min,max))
bin_width = 0.01
print (bin_width)
bins_array = np.arange(min, max+bin_width, bin_width)
#plt.subplot(3,2,4)
plt.hist(target_list, bins=bins_array)
plt.title('p_log-random vs random') 
plt.ylabel('frequency') 
plt.show()