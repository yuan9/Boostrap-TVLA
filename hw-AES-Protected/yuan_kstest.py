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
i = 0
while i < test_trace:
#while i < len(meta):

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
		
    i=i+1
		
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
Dpaws.TraceWrite(tr, tracefile='yuan_ks_test.dwfm')
	
