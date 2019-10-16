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

import time

start_time = time.time()

strt_pt = 0
stop_pt = 350000
sample_num = 350000
#Yuan: resolution of the power value
resolution = 256
test_trace = 1000
test_sample = 350000

i= 0
j =0
X=[]
Y=[]
overthr_count  = []
max = []
print ("readin files")

with open('log.dwdb') as file:
    content = file.readlines()
print ("finish reading files")
    
meta = []

for line in content:
    #print ("reach here")
    meta.append(dwdb_reader.parse_metadata_line(line))
    #meta.append(Dpaws.parse_metadata_line(line))
# print(meta[0])
# print ("total length:")
# print (len(meta))
list_fix = []
list_rand = []

step = 200
trace_start = 0
trace_stop = trace_start + step

while trace_stop < test_trace + 1: 
    print("trace_start:" + str(trace_start))
    print("trace_stop:" + str(trace_stop))
    for i in range(trace_start, trace_stop):
        X.append(dwdb_reader.read_trace(meta[i]['filename']))

        label = meta[i]['classifiers'].strip('{}')
        # print (str(i)+":" + str(X[i])+ "-" + label)
        #print (len(X[0]))
        #print (label)
	    #Yuan: read in one trace and update the histogram horizontally
        #print(i)
        if label == '1':
		    list_rand.append(X[i])
        if label == '0':
            list_fix.append(X[i])
		

		
    #print(list_fix)
    #print(list_rand)
    p_kstest = []
    for i in range(0, test_sample):
        test_fix = []
        test_rand = []
        for j in range(0,len(list_fix)):
            #print("j:" + str(j))	
            test_fix.append(list_fix[j][i])
		
        for k in range(0,len(list_rand)):
            #print("k:" + str(k))	
            test_rand.append(list_rand[k][i])
        #print(test_fix)
        #print(test_rand)
	
        d, p = stats.ks_2samp(test_fix, test_rand)
        print (p)
        p_kstest.append(p)
        print("----finish processing sample-" + str(i)+"--------")

    #print(p_kstest)
    tr = np.array(p_kstest)
    Dpaws.TraceWrite(tr, tracefile='ks_result/ks_revolution_p/yuan_ks_p{}.dwfm'.format(trace_stop))

#----------------------------------------------------------------------------------#
# Yuan: generate p-log value
#-----------------------------------------------------------------------------------#

    p_value2 = []
    small_value = 1e-323

    #p_min = np.amin(p_value)
    counter = 0
    for i in range(0, len(p_kstest)):
        if p_kstest[i] > small_value:
            p_value2.append(p_kstest[i])
        else:
            p_value2.append(small_value)
	    #p_value2.append(tr[i])
        if tr[i] < 0.000001:
            counter = counter + 1

    p_value_log = -np.log10(p_value2)
    overthr_count.append(counter)
    max.append(np.amax(p_value_log))
    print("max_ks:" + str(np.amax(p_value_log)))
    print("count_ks:" + str(counter))
    tr = np.array(p_value_log)
    Dpaws.TraceWrite(tr, tracefile='ks_result/ks_revolution_plog/yuan_ks_plog{}.dwfm'.format(trace_stop))


    trace_start = trace_start + step
    trace_stop =  trace_stop + step
	
np.savetxt("ks_result/ks_leak_count.txt", overthr_count, fmt='%s')
np.savetxt("ks_result/ks_leak_max.txt", max, fmt='%s')