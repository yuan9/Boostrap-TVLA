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

trace_num = 50000
start_sample = 10
end_sample =  11
step =  1000

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

pc_evolution = []
x_axis = []
for i in range(1, int(trace_num/step)+1):
 
	trace_range =  i * step 
	x_axis.append(trace_range)
	print("attacking on {} traces".format(trace_range))
	data_trans = data_np[0:trace_range].T
	classifiers_trans = classifiers2[0:trace_range].T

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
	#print(pc_all_abs[0])
	pc_evolution.append(pc_all_abs[0])

pc_evolution_trans =  (np.asarray(pc_evolution)).T
#print (pc_evolution_trans)

np.savetxt('pc.txt',pc_all_abs,fmt = '%s', delimiter=',')


#---------------------------------------------#
# Yuan: for ploting correlation coeffitient evolution
#---------------------------------------------#

font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'


plt.xlabel('Trace Number');
plt.ylabel('Correlation Coeffitient');

for i in range(0, len(pc_evolution_trans)):
	if i == 74:
		plt.plot(x_axis, pc_evolution_trans[i], linewidth=1.5, linestyle='-', color = 'r', zorder=255)	
	else:
		plt.plot(x_axis, pc_evolution_trans[i], linewidth=1.5, linestyle='-', color = 'grey', zorder = i)	
	

plt.show()

#plt.plot(data_np[0], linewidth=2, linestyle='-', color = 'Navy')
#plt.show()