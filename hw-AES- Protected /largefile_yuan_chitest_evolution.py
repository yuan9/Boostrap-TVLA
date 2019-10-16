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
import os, os.path, time, traceback

start_time = time.time()

strt_pt = 35
stop_pt = 215
test_sample =  stop_pt - strt_pt 
#test_sample =  3
test_trace = 300
sample_num = stop_pt - strt_pt + 1

#Yuan: resolution of the power value
resolution = 256
overthr_count  = []
max = []
result_dir = time.strftime("chi_test" + "-%Y-%m-%d_%H_%M")

#-------------------------------------------------------------------------------------------#
# Yuan: histogram generation
#-------------------------------------------------------------------------------------------#
hist_rand = {}
hist_fix = {}
list_rand = [[0 for x in range(0,resolution)] for y in range(0,test_sample)]
list_fix = [[0 for x in range(0,resolution)] for y in range(0,test_sample)]
print("finish initialization of histogram")
#print("len list_fix:{}".format(len(list_fix[0])))

#-------------------------------------------------------------------------------------------#
# Yuan: update histogram
#-------------------------------------------------------------------------------------------#
step = 100
os.mkdir(result_dir)
f_max = open(result_dir+'/chi_leak_max.txt', "a+")
f_count = open(result_dir+'/chi_leak_count.txt', "a+")
with open('merge.dwdb') as file:
    for cnt, line in enumerate(file):
        if cnt > test_trace:
          break
        else:
          #print("line{}:{}".format(cnt,line))
          line2 = dwdb_reader.parse_metadata_line(line)
          trace = dwdb_reader.read_trace(line2['filename'])[strt_pt:stop_pt]
          trace = trace.real.astype(int)
          #Yuan: notice add an offset value for the traces. 
          trace = trace + 128
          #print(len(trace))
          label = line2['classifiers'].strip('{}')
          #print("{}-{}".format(trace[0:test_sample],label))
          #print(label)
          if label == '1':
		      #Yuan: iterate each of the sample, can fix with the stop sample and start sample
		      #for j in range(strt_pt, stop_pt):
		      #print ("reach label 1")
              #for j in range(0, test_sample):
              for j in range(0,len(trace)):
			      # print ("j:" + str(j))
                  value = trace[j]
			      # print ("label1-j:"+ str(j) + "-value:" + str(value))
			      #Yuan: update the histogram
			      #print (str(list_rand[j][value]))

                  list_rand[j][value] = list_rand[j][value] + 1
			      #print (list_rand[0:1])
			      #print (str(list_rand[j][value]))
			      # print ("list_rand: {}".format(list_rand[0]))
			      # print ("list_fix:")
			      # print (list_fix[0])
          if label == '0':
		      #print ("reach label 0")
		      #Yuan: iterate each of the sample, can fix with the stop sample and start sample
              #for j in range(0, test_sample):
              for j in range(0,len(trace)):
		      #for j in range(strt_pt, stop_pt):
                  #print(j)
                  value = trace[j]
			      #print ("label0-j:"+ str(j) + "-value:" + str(value))
			      #print (str(list_fix[j][value]))
			      #Yuan: update the histogram 
                  list_fix[j][value] = list_fix[j][value] + 1

  #test_value = 127

  #print ("rand-"+str(test_value)+":"+ str(list_rand[0][test_value]))
  #print ("fix-"+str(test_value)+":" + str(list_fix[0][test_value]))
          if cnt!=0 and cnt%step == 0:
              print("{}-------------------------".format(cnt))    
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
	              #print("----finish processing sample" + str(i)+"--------")
	
  # print(p_value)
   
  #Yuan; writing a trace back
              tr = np.array(p_value)
              Dpaws.TraceWrite(tr, tracefile=result_dir+'/chi_revolution/yuan_chi_test-{}.dwfm'.format(cnt))
              p_value2 = []
              small_value = 1e-323

              #p_min = np.amin(p_value)
              counter = 0
              for i in range(0, len(p_value)):
                  if p_value[i] > small_value:
                      p_value2.append(p_value[i])
                  else:
                      p_value2.append(small_value)
	              #p_value2.append(tr[i])
                  if p_value[i] < 0.000001:
                      counter = counter + 1

              p_value_log = -np.log10(p_value2)
              #p_value_float64 = np.float64(p_value)
              #pt = meta['[]']
              #print(p_value[0:10])
              # # print(p_value_inv[0:3])
              #print(p_value_log[0:10])
              #overthr_count.append(counter)
             # max.append(np.amax(p_value_log))
              print("max_chi:" + str(np.amax(p_value_log)))
              print("count_chi:" + str(counter))
              f_max.write("{}:{}\n".format(cnt, np.amax(p_value_log)))
              f_count.write("{}:{}\n".format(cnt, counter))
              tr = np.array(p_value_log)
              Dpaws.TraceWrite(tr, tracefile=result_dir+'/chi_revolution_plog/yuan_chi_plog-{}.dwfm'.format(cnt))
            
#np.savetxt(result_dir+'/leak_count.txt', overthr_count, fmt='%s')
#np.savetxt(result_dir+'/leak_max.txt', max, fmt='%s')

f_count.close()
f_max.close()
   
#Yuan; writing a trace back




print("---%s seconds -----" %(time.time()-start_time))