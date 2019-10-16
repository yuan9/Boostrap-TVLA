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
import random
import array

import time

start_time = time.time()

strt_pt = 28371
stop_pt = 30950
#strt_pt = 16320
#stop_pt = 16420
sample_num = 350000
#Yuan: resolution of the power value
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

#----------------------------------------------------------------------------#
# Calculation based on the observed value
#----------------------------------------------------------------------------#
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
#print(X)		
#print(list_fix)
#print(list_rand)
p_ttest = []

for i in range(strt_pt, stop_pt):
#for i in range(0, test_sample):
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
	
    #t, p = stats.ttest_ind(test_fix, test_rand,equal_var=False)
    t, p = stats.ttest_ind(test_rand,test_fix ,equal_var=False)
    #print (p)
    p_ttest.append(p)
    print("----finish processing sample-" + str(i)+"--------")
	
#print("p_ttest")
#print(p_ttest)
tr = np.array(p_ttest)
Dpaws.TraceWrite(tr, tracefile='bootstrapping/boot_round1/p_ttest_obsv.dwfm')
	
#----------------------------------------------------------------------------#
# Bootstrapping procedure
#----------------------------------------------------------------------------#
bootnum = 10000
X_boot = []
list_rand_boot = []
list_fix_boot = []
boot_all = []
#rw = Dpaws.DatasetWriter( 'bootstrapping/boot.dwdb' , 'bootstrapping/boot_traces/b000.dwfm', '.' );
for b in range(464,5000 ):
    for i in range(0, test_trace):
    #while i < len(meta):
        rand = random.randint(0, test_trace-1)
        #print (rand)
        X_boot.append(dwdb_reader.read_trace(meta[rand]['filename']))

        label = meta[rand]['classifiers'].strip('{}')
        # print (str(i)+":" + str(X[i])+ "-" + label)
        #print (len(X[0]))
        #print (label)
	    #Yuan: read in one trace and update the histogram horizontally
        #print(i)
        if label == '1':
		    list_rand_boot.append(X_boot[i])
        if label == '0':
            list_fix_boot.append(X_boot[i])

    #print (X_boot)	
    #print(list_fix_boot)
    #print(list_rand_boot)
    p_ttest_boot = []

    for i in range(strt_pt, stop_pt):
    #for i in range(0, test_sample):
        test_fix_boot = []
        test_rand_boot = []
        for j in range(0,len(list_fix_boot)):
            #print("j:" + str(j))
            #print (list_fix_boot[j][i])	
            test_fix_boot.append(list_fix_boot[j][i])
		
        for k in range(0,len(list_rand_boot)):
            #print("k:" + str(k))
            #print (list_rand_boot[k][i])	
            test_rand_boot.append(list_rand_boot[k][i])
        #print(test_fix_boot)
        #print(test_rand_boot)
	
        t_boot, p_boot = stats.ttest_ind(test_fix_boot, test_rand_boot,equal_var = False)
        #print (p_boot)
        p_ttest_boot.append(p_boot)
        #print("----BOOT-" + str(b) + "finish processing sample-" + str(i)+"--------")
    #print("p_ttest_boot:")
    #print(p_ttest_boot)
    tr = np.array(p_ttest_boot)
    Dpaws.TraceWrite(tr, tracefile='bootstrapping/boot_round1/yuan_boot_tp{}.dwfm'.format(b))
    print("******FINISH BOOT" + str(b)+"*******")
    # tr2 = []
    # p_ttest_boot2 = [''.join(item) for item in tr.astype(str)]
    # print("p_ttest_boot2:")
    # print (p_ttest_boot2)
    # for item in p_ttest_boot2:
        # tr2.append(item)
    # print("tr2:")
    # print(tr2)
    # #tr2 = array.array(p_ttest_boot2)
    # #for item in p_ttest_boot2('')
	
	#Yuan:write dwdb file
    # wr = rw.NewRecord()
    # wr.AddData(tr)
    # rw.SubmitRecord(wr)
	
    # boot_all.append(p_ttest_boot)
#print (boot_all)

print("---%s seconds -----" %(time.time()-start_time))