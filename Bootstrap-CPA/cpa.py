from __future__ import absolute_import, division, print_function, with_statement

import numpy as np
import os
import re
import struct
import functools
import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

#import tensorflow as tf
#import keras

#import aes_internals as aise
#import dwdb_reader
 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import time
import util.dwdb_reader as io
import util.tests as tests

trace_num = 40000
start_sample = 50
end_sample =  11


dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/Bootstrap-CPA/trace.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/Bootstrap-CPA/')
data_batch, meta_batch = dsr.read_batch(trace_num, start_sample, end_sample)
data_np = np.asarray(data_batch)

#processing of classifiers
classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('hw=')]
classifiers= np.asarray(classifiers)
_classrifiers = []
for hw in classifiers:
	_classrifiers.append(hw.split(','))

classifiers2 =  (np.asarray(_classrifiers)).astype(int)

data_trans = data_np.T
classifiers_trans = classifiers2.T

# print ("data original: {}".format(data_np))
# print ("data trans:{}".format(data_trans))
# #print (classifiers)
# print ("classifiers2:{}".format(classifiers2))
# print ("classifiers trns:{}".format(classifiers_trans))

pc_all = []
for sample in data_trans:
	pc_sample = []
	for keyguess in classifiers_trans:
		#print ("{}-{}".format(sample, keyguess))
		pc, p = stats.pearsonr(sample, keyguess)
		pc_sample.append(pc)

	pc_all.append(pc_sample)

pc_all_np =  np.asarray(pc_all)
pc_all_abs = np.absolute(pc_all_np)
#print(pc_all_np)
print(pc_all_abs)

maxValue = np.nanmax(pc_all_abs)
#print(maxValue)

# Find index of maximum value from 2D numpy array
result = np.where(pc_all_abs == np.nanmax(pc_all_abs))
 
#print('Tuple of arrays returned : ', result)
 
#print('List of coordinates of maximum value in Numpy array : ')
# zip the 2 arrays to get the exact coordinates
listOfCordinates = list(zip(result[0], result[1]))
# travese over the list of cordinates
for cord in listOfCordinates:
    print(cord)
np.savetxt('pc.txt',pc_all_abs,fmt = '%s', delimiter=',')

#plt.plot(data_np[0], linewidth=2, linestyle='-', color = 'Navy')
#plt.show()