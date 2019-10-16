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
import DpawsUtils
import DpawsTools 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
import random
import array
from scipy.stats import norm
import time

start_time = time.time()

strt_pt = 40000
stop_pt = 45000
#strt_pt = 41500
#stop_pt = 43000
test_sample = stop_pt - strt_pt 
#test_sample = 3
test_trace = 2000



overthr_count = []
max = []
#result_dir = time.strftime("ks_test" + "-%Y-%m-%d_%H_%M")
#result_dir_t = time.strftime("boot"+ str(test_trace) +"-sample"+ str(strt_pt) + "-" + str(stop_pt) + "-%Y-%m-%d_%H_%M")
result_dir_t = time.strftime("boot2000-sample40000-45000-2019-07-18_13_46")
list_fix = []
list_rand = []

overthr_count = []
max = []

overthr_count_t = []
max_t = []
tvalue = []

#----------------------------------------------------------------------------#
# Calculation based on the observed value
#----------------------------------------------------------------------------#
#trace_set = []
#label_set = []
#binave = DpawsTools.Binave(test_sample, 1)
#with open('log.dwdb') as file:
#     for cnt, line in enumerate(file):
#         if cnt > test_trace:
#             break
#         else:
#             #print(cnt)
#             #print("line{}:{}".format(cnt,line))
#             line2 = dwdb_reader.parse_metadata_line(line)
#             trace = dwdb_reader.read_trace(line2['filename'])[strt_pt:stop_pt]
#             trace = trace.real.astype(int)
#                     #Yuan: notice add an offset value for the traces.
#             trace = trace + 128
#             #trace = dwdb_reader.read_trace(line2['filename'])[0:3]
#             label = line2['classifiers'].strip('{}')
#             #print("{}-{}".format(trace[0:test_sample],label))
#             #print("trace-{}".format(cnt))
#             trace_set.append(trace)
#             label_set.append(label) 
#             binave.process(trace_set, label_set)
#             trace_set = []
#             label_set = []

#             if label == '1':
#		             list_rand.append(trace)
#             if label == '0':
#                 list_fix.append(trace)
            
#             #print("list_fix:{}".format(list_fix))
#             #print("list_rand:{}".format(list_rand))
#             list_fix_np = np.array(list_fix)
#             list_rand_np = np.array(list_rand)

#             #print("list_fix_np:{}".format(list_fix_np))
#             #print("list_rand_np:{}".format(list_rand_np))
#             list_fix_np_trans = np.transpose(list_fix_np)
#             list_rand_np_trans = np.transpose(list_rand_np)
#             #print("list_fix_np_TRANS:{}".format(list_fix_np_trans))
#             #print("list_rand_np_TRANS:{}".format(list_rand_np_trans))
            
#             p_ttest = []
#             p_ttest2 = []
#             small_value = 1e-323
#             for i in range(0,len(list_fix_np_trans)):
#                 d_t, p_t = stats.ttest_ind(list_fix_np_trans[i], list_rand_np_trans[i], equal_var = False)
#                 tvalue.append(d_t)
#                 if p_t > small_value:
#                     p_ttest2.append(p_t)
#                 else:
#                     p_ttest2.append(small_value)


# #print(len(list_fix_np))
# #print(len(list_rand_np)) 
#tt = next(binave.ttests(1))
#Dpaws.TraceWrite(tt, tracefile=result_dir_t + '/t_ttest-obsr.dwfm')
##print("binave:{}".format(tt[0:5]))
##print("should be p value:{}".format(p_ttest2[0:5]))
#t_abs = np.absolute(tt)
#t_p = 2 * (1 - norm.cdf(t_abs))
##print(t_p[0:5])
#tr = np.array(p_ttest2)
#Dpaws.TraceWrite(tr, tracefile=result_dir_t + '/p_ttest-obsr.dwfm')
#tr_log = np.array(-np.log10(p_ttest2))
#Dpaws.TraceWrite(tr_log, tracefile=result_dir_t + '/p_ttest-obsr-log.dwfm')


#----------------------------------------------------------------------------#
# Bootstrapping procedure
#----------------------------------------------------------------------------#
bootnum = 10000
numbers =[]

list_fix = []
list_rand = []
label_set=[]
trace_set=[]
# X_boot = []
# list_rand_boot = []
# list_fix_boot = []
# boot_all = []
# #rw = Dpaws.DatasetWriter( 'bootstrapping/boot.dwdb' , 'bootstrapping/boot_traces/b000.dwfm', '.' );
#os.mkdir(result_dir_t)
f_count = open(result_dir_t+'/boot_leak_count.txt', "a+")
#binave = DpawsTools.Binave(test_sample, 1)
for b in range(2894,bootnum):
    rand_numbers = []
    dic_rand = {}
    binave = DpawsTools.Binave(test_sample, 1)
    for i in range(0,test_trace-1):     
        #rand_numbers.append(random.choice(numbers))
        rand = random.randint(0, test_trace-1)
        #rand = i
        #rand_numbers.append(rand)
        if rand not in dic_rand:
            dic_rand[rand] = 1
        else:
            dic_rand[rand] = dic_rand[rand] + 1
    rand_numbers = list(dic_rand.keys())
    rand_numbers.sort()
    #print ("random_numbers:{}".format(rand_numbers))
    #print ("random_dic:{}".format(dic_rand))
    
    with open('log.dwdb') as file:
        for cnt, line in enumerate(file):
            if cnt > test_trace:
                break
            elif cnt in rand_numbers:

                for k in range(0,dic_rand[cnt]):
                    #print (cnt)
                    line2 = dwdb_reader.parse_metadata_line(line)
                    trace = dwdb_reader.read_trace(line2['filename'])[strt_pt:stop_pt]
                    trace = trace.real.astype(int)
                    #Yuan: notice add an offset value for the traces. 
                    trace = trace + 128
                    #print(len(trace))
                    trace_set.append(trace)
                    label = line2['classifiers'].strip('{}')
                    label_set.append(label)
                    #print ("{}-{}".format(trace_set[0][0:3],label))

                    binave.process(trace_set, label_set)
                    trace_set = []
                    label_set = []

    tt = next(binave.ttests(1))
    t_abs = np.absolute(tt)
    t_p = 2*(1- norm.cdf(t_abs))
    t_p2 = []
    counter = 0
    #post processing
    small_value = 1e-323
    for i in range(0, len(t_p)):
        if t_p[i] > small_value:
            t_p2.append(t_p[i])
        else:
            t_p2.append(small_value)
        if t_p[i] < 0.000001:
            counter = counter + 1
      
    t_p_log = -np.log10(t_p2)
    f_count.write("{}:{}\n".format(b, counter))
    Dpaws.TraceWrite(tt, tracefile= result_dir_t+'/boot_t/t_ttest_boot-{}.dwfm'.format(b))
    Dpaws.TraceWrite(t_p2, tracefile= result_dir_t+'/boot_p/p_ttest_boot-{}.dwfm'.format(b))
    Dpaws.TraceWrite(t_p_log, tracefile= result_dir_t+'/boot_p_log/plog_ttest_boot-{}.dwfm'.format(b))
    print("******FINISH BOOT" + str(b)+"*******")  
    print("---%s seconds -----" %(time.time()-start_time))