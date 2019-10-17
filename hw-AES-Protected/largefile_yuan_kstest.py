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
step = 100
list_fix = []
list_rand = []

overthr_count  = []
max = []

overthr_count_t  = []
max_t = []

#ifile = None # 'merge_100.dwdb'
#file = open(ifile) if ifile else sys.stdin

with open('log.dwdb') as file:
    for cnt, line in enumerate(file):
#for i, line in enumerate(file):
        if cnt > test_trace:
            break
        else:
            #print("line{}:{}".format(cnt,line))
            line2 = dwdb_reader.parse_metadata_line(line)
            trace = dwdb_reader.read_trace(line2['filename'])[strt_pt:stop_pt]
            trace = trace.real.astype(int)
            #Yuan: notice add an offset value for the traces. 
            trace = trace + 128
        
            label = line2['classifiers'].strip('{}')
            #print("{}-{}".format(trace[0:test_sample],label))
            #print("trace-{}".format(cnt))
    
            if label == '1':
		        list_rand.append(trace)
            if label == '0':
                list_fix.append(trace)

    #print("list_fix:{}".format(list_fix))
    #print("list_rand:{}".format(list_rand))
            if cnt!=0 and (cnt+1)%step == 0:
                print("{}-------------------------".format(cnt))
                p_kstest = []
                p_ttest = []
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
                    d_t, p_t = stats.ttest_ind(test_fix, test_rand, equal_var = False)
                    #print (p)
                    p_kstest.append(p)
                    p_ttest.append(p_t)
                    #print("----finish processing sample-" + str(i)+"--------")
                tr = np.array(p_kstest)
                Dpaws.TraceWrite(tr, tracefile=result_dir+'/ks_evolution/yuan_ks_test-{}.dwfm'.format(int(cnt)))
                tr2 = np.array(p_ttest)
                Dpaws.TraceWrite(tr2, tracefile=result_dir_t+'/t_evolution/yuan_t_test-{}.dwfm'.format(int(cnt)))

                p_value2 = []
                small_value = 1e-323
                p_value2_t = []

                #p_min = np.amin(p_value)
                counter_t = 0
                #p_min = np.amin(p_value)
                counter = 0
                for i in range(0, len(p_kstest)):
                    if p_kstest[i] > small_value:
                        p_value2.append(p_kstest[i])
                    else:
                        p_value2.append(small_value)
	                #p_value2.append(tr[i])
                    if p_kstest[i] < 0.000001:
                        counter = counter + 1

                    if p_ttest[i] > small_value:
                        p_value2_t.append(p_ttest[i])
                    else:
                        p_value2_t.append(small_value)
	                #p_value2.append(tr[i])
                    if p_ttest[i] < 0.000001:
                        counter_t = counter_t + 1

                p_value_log = -np.log10(p_value2)
                p_value_log_t = -np.log10(p_value2_t)
                #p_value_float64 = np.float64(p_value)
                #pt = meta['[]']
                #print(p_value[0:10])
                # # print(p_value_inv[0:3])
                #print(p_value_log[0:10])
                overthr_count.append(counter)
                max.append(np.amax(p_value_log))
                print("max_ks:" + str(np.amax(p_value_log)))
                print("count_ks:" + str(counter))
                tr = np.array(p_value_log)
                Dpaws.TraceWrite(tr, tracefile=result_dir+'/ks_evolution_plog/yuan_ks_plog-{}.dwfm'.format(int(cnt)))

                overthr_count_t.append(counter_t)
                max_t.append(np.amax(p_value_log_t))
                print("max_t:" + str(np.amax(p_value_log_t)))
                print("count_t:" + str(counter_t))
                tr_t = np.array(p_value_log_t)
                Dpaws.TraceWrite(tr_t, tracefile=result_dir_t+'/t_evolution_plog/yuan_t_plog-{}.dwfm'.format(int(cnt)))

np.savetxt(result_dir+'/ks_leak_count.txt', overthr_count, fmt='%s')
np.savetxt(result_dir+'/ks_leak_max.txt', max, fmt='%s') 

np.savetxt(result_dir_t+'/t_leak_count.txt', overthr_count_t, fmt='%s')
np.savetxt(result_dir_t+'/t_leak_max.txt', max_t, fmt='%s')            
