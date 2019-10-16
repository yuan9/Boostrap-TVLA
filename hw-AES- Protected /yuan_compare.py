# To support both python 2 and python 3
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

import aes_internals as aise
import dwdb_reader
import Dpaws 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm

#-----------------------------------------------------------------------------------#
#  Chi-square test
#-----------------------------------------------------------------------------------#
meta = {}
p_value2 = []
small_value = 1e-323
p_value = Dpaws.TraceRead('yuan_chi_test.dwfm', metadata=meta)
#p_min = np.amin(p_value)
counter = 0
for i in range(0, len(p_value)):
	p_value2.append(max(p_value[i],small_value))
	if p_value[i] < 0.000001:
		counter = counter + 1
		
p_value_log = -np.log10(p_value2)
#p_value_float64 = np.float64(p_value)
#pt = meta['[]']
#print(p_value[0:10])
# # print(p_value_inv[0:3])
#print(p_value_log[0:10])
print("max_chi:" + str(np.amax(p_value_log)))
print("count_chi:" + str(counter))
tr = np.array(p_value_log)
Dpaws.TraceWrite(tr, tracefile='yuan_chi_p.dwfm')

#print(p_value_float64[0:3])

# p_norm=[]
# p_min = np.amin(p_value)
# print (p_min)
# p_value_sub = np.float() - p_min
# print(p_value[0:3])
# print(p_value_sub[0:3])
# # transfer to standard normal distribution
# # for i in range(0, len(p_value)):
	# # value =  1-p_value[i]/2
	# # print (value)
	# # normal = norm.ppf(1-p_value[i]/2)
	# # p_norm.append(normal)
# tr = np.array(p_norm)
# Dpaws.TraceWrite(tr, tracefile='yuan_chi_test_norm.dwfm')

#-----------------------------------------------------------------------------------#
#  t-test test
#-----------------------------------------------------------------------------------#
meta = {}
t_p2 =[]
t = Dpaws.TraceRead('tvla_yuan_v000', metadata=meta)
t_abs = np.absolute(t)
t_p = 2*(1- norm.cdf(t_abs))
counter2 = 0
for i in range(0, len(t_p)):
	t_p2.append(max(t_p[i],small_value))
	if t_p[i] < 0.000001:
		counter2 = counter2 + 1
		
t_p_log = -np.log10(t_p2)
# print(t[0:3])
# print(t_abs[0:3])
#print(t_p[0:10])
#print(t_p_log[0:10])
print("max_t:" + str(np.amax(t_p_log)))
print("count_t:" + str(counter2))
#print(np.amax(t_p_log))
tr = np.array(t_p_log)
Dpaws.TraceWrite(tr, tracefile='yuan_t_p.dwfm')


#-----------------------------------------------------------------------------------#
#  k-s test
#-----------------------------------------------------------------------------------#
meta = {}
ks_p2 = []
ks_p_log = []
ks_p = Dpaws.TraceRead('yuan_ks_test.dwfm', metadata=meta)
counter3 = 0
for i in range(0, len(ks_p)):
	ks_p2.append(max(t_p[i],small_value))
	if ks_p[i] < 0.000001:
		counter3 = counter3 + 1
ks_p_log = -np.log10(ks_p2)

print("max_ks:" + str(np.amax(ks_p_log)))
print("count_ks:" + str(counter3))

tr = np.array(ks_p_log)
Dpaws.TraceWrite(tr, tracefile='yuan_ks_p.dwfm')