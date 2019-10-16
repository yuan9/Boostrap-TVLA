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
from scipy.stats import chi2_contingency
from scipy.stats import norm
import time
import os, os.path, time, traceback

start_time = time.time()

strt_pt = 0
stop_pt = 100000
test_sample =  stop_pt - strt_pt 
#test_sample =  3
test_trace = 100000
sample_num = stop_pt - strt_pt + 1

#Yuan: resolution of the power value
resolution = 256
overthr_count  = []
max = []
result_dir = time.strftime("ks_test" + "-%Y-%m-%d_%H_%M")
result_dir_t = time.strftime("t_test" + "-%Y-%m-%d_%H_%M")
list_fix = []
list_rand = []

overthr_count  = []
max = []

overthr_count_t  = []
max_t = []

trace_set = []
label_set = []

result_dir_t = time.strftime("t-test" + "-%Y-%m-%d_%H_%M")

step = 5000
os.mkdir(result_dir_t)
f_count = open(result_dir_t+'/ttest_leak_count.txt', "a+")

binave = DpawsTools.Binave(test_sample, 1)
with open('log.dwdb') as file:
    for cnt, line in enumerate(file):
        if cnt > test_trace:
            break
        else:
            line2 = dwdb_reader.parse_metadata_line(line)
            trace = dwdb_reader.read_trace(line2['filename'])[strt_pt:stop_pt]
            #trace = dwdb_reader.read_trace(line2['filename'])[0:3]
         
            trace = trace.real.astype(int)
            trace = trace + 128
            trace_set.append(trace)
            label = line2['classifiers'].strip('{}')
            label_set.append(label) 
            binave.process(trace_set, label_set)
            trace_set = []
            label_set = []

            if cnt!=0 and (cnt+1)%step == 0:
                  print("evolution------{}".format(cnt))
                  tt = next(binave.ttests(1))
                  t_abs = np.absolute(tt)
                  t_p = 2*(1- norm.cdf(t_abs))
                  t_p2 = []
                  counter = 0

                  small_value = 1e-323
                  for i in range(0, len(t_p)):
                      if t_p[i] > small_value:
                          t_p2.append(t_p[i])
                      else:
                          t_p2.append(small_value)
                  if t_p[i] < 0.000001:
                          counter = counter + 1
      
                  t_p_log = -np.log10(t_p2)
                  f_count.write("{}:{}\n".format(cnt, counter))
                  Dpaws.TraceWrite(tt, tracefile= result_dir_t+'/ttest_t/t_ttest-{}.dwfm'.format(cnt))
                  Dpaws.TraceWrite(t_p2, tracefile= result_dir_t+'/ttest_p/p_ttest-{}.dwfm'.format(cnt))
                  Dpaws.TraceWrite(t_p_log, tracefile= result_dir_t+'/ttest_p_log/plog_ttest-{}.dwfm'.format(cnt))
f_count.close()