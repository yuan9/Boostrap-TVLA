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


tracenum = 50000
#Yuan: Note that the basic range is from (40,180)
sample_start = 40 
sample_end = 180

#sample_start = 0
#sample_end = 3
dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/RawTraces_new.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/')
data_batch, meta_batch = dsr.read_batch(tracenum, sample_start, sample_end)
data_np = np.asarray(data_batch)
print(len(data_np[0]))
#processing of classifiers
classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('s=')]
classifiers= np.asarray(classifiers) # 2D numpy array of classifier
print("finish readin traces")

t_evolution = []


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
for i in range(0, sample_end - sample_start):
	t, p = stats.ttest_ind(rand_trans[i], fix_trans[i], equal_var = False)
	t_value.append(abs(t))

# data = np.ones_like(data_np[0])
# data_label = np.ones_like(classifiers[0])
# print (data)
# print (data_label)
#print (classifiers)
#print (data_batch[1])

font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'

plt.xlabel('Time');
plt.ylabel('t-statistics');

print(t_value)
plt.plot(t_value,linewidth=2, linestyle='-',  color = 'navy')
plt.axhline(y=4.5, color='r', linewidth=2)
plt.ylim(top = 10 )
# plt.plot(t_evolution[0])
# plt.plot(t_evolution[1])
# plt.plot(t_evolution[2])
# plt.axhline(y=4.5, color='r')
# plt.axvline(x=83,  color='b')
# #plt.legend(['10000','20000', '30000'], loc='upper left')
# plt.legend(legend, loc='upper left')


plt.show()
