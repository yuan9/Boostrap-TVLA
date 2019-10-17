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
import time

start_time = time.time()

strt_pt = 0
stop_pt = 350000
sample_num = 350000
#Yuan: resolution of the power value
resolution = 256

test_sample = 350000
test_trace = 1000
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
# print ("list_fix:")
# print (list_fix[1])
# print ("list_rand:")
# print (list_rand[1])
# test_value =102
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


i = 0
j = 0
p_value = []
for i in range(0,test_sample):
	list_fix_no0 = []
	list_rand_no0 = []
    #print (i)
	#remove the 0 entry in the contigency table
	for j in range(0, resolution):	
		#print(j)
		if (list_fix[i][j] + list_rand[i][j] != 0):
			list_fix_no0.append(list_fix[i][j])
			list_rand_no0.append(list_rand[i][j])


	# print ("list_fix_after:")
	# print (list_fix_no0)
	# print ("list_rand_after:")
	# print (list_rand_no0)
	

    #increase move together entries
	#for i in range(0,len(list_fix_no0)):
	k = 0
	while (list_fix_no0[k] < 5 or list_rand_no0[k] < 5):
		list_fix_no0[k + 1] = list_fix_no0[k] + list_fix_no0[k + 1]
		list_rand_no0[k + 1] = list_rand_no0[k] + list_rand_no0[k + 1]
		k = k + 1
				
	# print ("list_fix_after1:")
	# print (list_fix_no0)
	# print ("list_rand_after1:")
	# print (list_rand_no0)
	
	k = len(list_fix_no0)-1
	#print (k)
	while (list_fix_no0[k] < 5 or list_rand_no0[k] < 5):
		list_fix_no0[k - 1] = list_fix_no0[k] + list_fix_no0[k - 1]
		list_rand_no0[k - 1] = list_rand_no0[k] + list_rand_no0[k - 1]
		k = k - 1
	# print ("list_fix_after2:")
	# print (list_fix_no0)
	# print ("list_rand_after2:")
	# print (list_rand_no0)
	
	list_fix_notail = []
	list_rand_notail = []
	k = 0
	for k in range(0, len(list_fix_no0)):
		if (list_fix_no0[k] >=5 and list_rand_no0[k] >= 5):
			list_fix_notail.append(list_fix_no0[k])
			list_rand_notail.append(list_rand_no0[k])
	# print ("list_fix_after3:")
	# print (list_fix_notail)
	# print ("list_rand_after3:")
	# print (list_rand_notail)
	obs =  np.array([list_fix_notail,list_rand_notail])
	chi, p, df, expctd = chi2_contingency(obs)
	# print(p)
	# print(df)
	p_value.append(p)
	print("----finish processing sample" + str(i)+"--------")
	
# print(p_value)
   
#Yuan; writing a trace back
tr = np.array(p_value)
Dpaws.TraceWrite(tr, tracefile='yuan_chi_test.dwfm')



print("---%s seconds -----" %(time.time()-start_time))