from __future__ import absolute_import, division, print_function, with_statement

import numpy as np
import os
import re
import struct
import functools
import time

import matplotlib
import matplotlib.pyplot as plt
#import pandas as pd

#import tensorflow as tf
#import keras

#import aes_internals as aise
import dwdb_reader
 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm
#import seaborn as sns
import random
import util.dwdb_reader as io
import util.tests as tests

result_dir = "fn_Bootevolution_1sample"
trace_range = 50000
step =  1000
# trace_range = 500
# step =  20

tracenum = 50000
#Yuan: Note that the basic range is from (40,180), this plot is for sample-83
sample_start = 40 + 83
sample_end = 40 +84

small_value =  1e-323
#sample_start = 0
#sample_end = 3
dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/RawTraces_new.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/')
data_batch, meta_batch = dsr.read_batch(tracenum, sample_start, sample_end)
data_np = np.asarray(data_batch)

#processing of classifiers
classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('s=')]
classifiers= np.asarray(classifiers) # 2D numpy array of classifier
print("finish readin traces")

t_evolution = []
plog_evolution = []
p_evolution = []

legend = []
for j in range(1, int(trace_range/step) + 1):
	tracenum = j * step
	legend.append(tracenum)
# initializing the rand and fix dataset
	rand = []
	fix = []
	for i in range(0, tracenum):
		if classifiers[i] == '1':
			rand.append(data_np[i])
		if classifiers[i] == '0':
			fix.append(data_np[i])
	#print("rand:{}".format(rand))
	#print("fix:{}".format(fix))

	rand_np = np.asarray(rand)
	rand_trans =  rand_np.T
	#print (rand_trans)

	fix_np = np.asarray(fix)
	fix_trans =  fix_np.T
	#print (fix_trans)

	# t-statistics
	t_value =[]
	p_value = []
	for i in range(0, sample_end - sample_start):
		t, p = stats.ttest_ind(rand_trans[i], fix_trans[i], equal_var = False)
		t_value.append(abs(t))
		p_value.append(max(p,small_value))
	t_evolution.append(t_value)
	p_evolution.append(p_value)
	# data = np.ones_like(data_np[0])
	# data_label = np.ones_like(classifiers[0])
	# print (data)
	# print (data_label)
	#print (classifiers)
	#print (data_batch[1])
	print ("finish the {}".format(tracenum))

t_evolution_flat =  (np.array(t_evolution)).flatten()
p_evolution_flat =  (np.array(p_evolution)).flatten()
plog_evolution = -np.log10(p_evolution_flat)

np.savetxt(result_dir+'/tplog-step{}-range{}.txt'.format(step, trace_range),plog_evolution,fmt = '%s', delimiter=',')


font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'


#---------------------------------------------#
# Yuan: for ploting t-statistics evolution
#---------------------------------------------#
plt.xlabel('Trace Number');
plt.ylabel('t-statistic');
plt.plot(legend, t_evolution_flat,linewidth=2, linestyle='-', color = 'Green')
plt.axhline(y=4.5, color='r',linewidth=2)
# plt.ylim(top = 10)

#---------------------------------------------#
# Yuan: for ploting p-value evolution
#---------------------------------------------#
plt.xlabel('Trace Number');
#plt.ylabel('-log10(p)');
plt.plot(legend, plog_evolution, linewidth=2, linestyle='-', color = 'Navy')
plt.axhline(y=5, color='r',linewidth=2)
#plt.ylim(top = 10)


plt.show()
