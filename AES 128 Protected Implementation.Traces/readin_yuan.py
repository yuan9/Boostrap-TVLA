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

#----------------------------------------------------------------------#
# Yuan: histogram generation
#----------------------------------------------------------------------#
i= 0
j =0
X=[]
y=[]
#list_rand =[][]
#list_fix = [][]
hist_rand = {}
hist_fix = {}

#Yuan: initialize the list of histogram ()
# for i in range(0,resolution):
    # hist_fix[i] = 0
    # hist_rand[i] = 0
	
# list_fix =  [ hist_fix for i in range(0,sample_num) ]
# list_rand = [ hist_rand for i in range(0,sample_num) ]	

#for i in range(0,sample_num):
# for i in range(0,2):
    # #for j in range(0,resolution):
	# for j in range(0,4):
		# hist_rand[i][j] = 0
		# hist_fix[j] = 0
	# list_rand.append(hist_rand)
	# list_fix.append(hist_fix)

list_rand = [[0 for x in range(0,resolution)] for y in range(0,sample_num)]
list_fix = [[0 for x in range(0,resolution)] for y in range(0,sample_num)]
#print (list_fix)
#print (list_rand)
# print (list_fix[0][4])

#Yuan: generate the histogram
# i: trace number j:sample number
i = 0
test_sample = 1
test_trace = 1000
while i < test_trace:
#while i < len(meta):
    #print("reach here")
    X.append(dwdb_reader.read_trace(meta[i]['filename']))
	#X.append(Dpaws.read_trace(meta[i]['filename']))
    print("finish processing trace-" + str(i))
    
    label = meta[i]['classifiers'].strip('{}')
    # print (str(i)+":" + str(X[i])+ "-" + label)
    #print (len(X[0]))
    #print (label)
	#Yuan: read in one trace and update the histogram horizontally
    if label == '1':
		#Yuan: iterate each of the sample, can fix with the stop sample and start sample
		#for j in range(strt_pt, stop_pt):
		#print ("reach label 1")
		for j in range(0, test_sample):
			# print ("j:" + str(j))
			value = X[i][j]
			# print ("label1-j:"+ str(j) + "-value:" + str(value))
			#Yuan: update the histogram
			#print (str(list_rand[j][value]))
			
			list_rand[j][value] = list_rand[j][value] + 1
			#print (list_rand[0:1])
			#print (str(list_rand[j][value]))
			# print ("list_rand:")
			# print (list_rand[0])
			# print ("list_fix:")
			# print (list_fix[0])
    if label == '0':
		#print ("reach label 0")
		#Yuan: iterate each of the sample, can fix with the stop sample and start sample
		for j in range(0, test_sample):
		#for j in range(strt_pt, stop_pt):
			value = X[i][j]
			#print ("label0-j:"+ str(j) + "-value:" + str(value))
			#print (str(list_fix[j][value]))
			#Yuan: update the histogram 
			list_fix[j][value] = list_fix[j][value] + 1
			#print (str(list_fix[j][value]))
			# print ("list_rand:")
			# print (list_rand[0])
			# print ("list_fix:")
			# print (list_fix[0])
							
    #y.append(meta[i]['classifiers'].strip('{}'))
    i=i+1
print ("list_fix:")
print (list_fix[0])
print ("list_rand:")
print (list_rand[0])
test_value =102
# print ("***************************************************")
# print ("rand-"+str(test_value)+":"+ str(list_rand[0][test_value]))
# print ("fix-"+str(test_value)+":" + str(list_fix[0][test_value]))
# print ("***************************************************")
# print ("rand-"+str(test_value)+":"+ str(list_rand[1][test_value]))
# print ("fix-"+str(test_value)+":" + str(list_fix[1][test_value]))
# # print ("rand-"+str(test_value)+":"+ str(list_rand[1][107]))
# # print ("fix-"+str(test_value)+":" + str(list_fix[1][107]))
# print ("***************************************************")
# print ("rand-"+str(test_value)+":"+ str(list_rand[2][test_value]))
# print ("fix-"+str(test_value)+":" + str(list_fix[2][test_value]))
# print ("***************************************************")
#-------------------------------------------------------------------------#
# chi-squrare calculation
#--------------------------------------------------------------------------#
i = 0
j = 0
p = []
for i in range(0,test_sample):
#with each sample, there is one total array
    print("sample:" + str(i))
    total_hori = []
    sum_fix= 0
    sum_rand=0
    #print(list_rand[i])    
    for j in range(0,resolution):
        sum = 0

        sum = list_rand[i][j] + list_fix[i][j]
        total_hori.append(sum)
        sum_fix = sum_fix + list_fix[i][j]
        sum_rand = sum_rand + list_rand[i][j]
	#for each sample, we calculate the sum_hori, sum_fix and sum_rand
    print ("total:"+ str(total_hori[test_value]))
    print ("sum_rand:" + str(sum_rand))
    print ("sum_fix:" + str(sum_fix))
    #expectation and chi value calculation
    e_rand = []
    e_fix = []
    chi_rand = []
    chi_fix = []
    k = 0
    for k in range(0, resolution):
	    # for the random set
        e = (total_hori[k] * sum_rand)/test_trace
        #print (str(k) + "+" + str(e))
        #print (str(k) + ":" + str(list_rand[i][k]))
        #print (str(k) + ":" + str(list_rand[i][k]-e))
        if e!=0:
            chi = ((list_rand[i][k]-e)*(list_rand[i][k]-e))/e
        else:
			chi = 0
        #print (str(k) + "-" + str(chi))
        e_rand.append(e)
        chi_rand.append(chi)
		#for the fix set
        e = (total_hori[k] * sum_fix)/test_trace
        if e!=0:
			chi = ((list_fix[i][k]-e)*(list_fix[i][k]-e))/e
        else:
			chi = 0
        e_fix.append(e)
        chi_fix.append(chi)
    # print ("rand_expectation:"+ str(e_rand[test_value]))
    # print ("fix_expectation:" + str(e_fix[test_value]))
    # print ("rand_chi:"+ str(chi_rand[test_value]))
    # print ("fix_chi:" + str(chi_fix[test_value]))
	
	#calculation of chi-square values:
    k=0
    chi_sum = 0
    for k in range(0,resolution):
        chi_sum = chi_rand[k] + chi_fix[k] + chi_sum
    print ("chi_sum:" + str(chi_sum))
	
	#calculate p-value:
    df =  resolution - 1
    p_value = float(chi2.sf(chi_sum, df))
    print (p_value)

    p.append(p_value)
    print("----finish processing sample" + str(i)+"--------")
print ("p:")
print (p)   
#Yuan; writing a trace back
tr = np.array(p)
Dpaws.TraceWrite(tr, tracefile='yuan_chi_test.dwfm')

print("---%s seconds -----" %(time.time()-start_time))

# fix_set=[]
# rand_set=[]

#X_np = np.array(X, dtype=np.int32)

# Yuan: seperate random and fix
# for i in range (0, len(X)):
    # if y[i] == '1':
		# rand_set.append(X[i])
    # else:
		# fix_set.append(X[i])
# print ('rand_set:')	
# print (len(rand_set))
# print ('fix_set:')	
# print (len(fix_set))
# X_np = np.array(X, dtype=np.int32)

# means = X_np.mean(axis=0, keepdims=True)
# stds = X_np.std(axis=0, keepdims=True) + 1e-10
# X_scaled = (X_np - means) / stds

# X_test, X_valid, X_train = X_scaled[:5000], X_scaled[5000:10000], X_scaled[10000:]

# print(X_train.shape)