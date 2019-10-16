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
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Dpaws
import DpawsUtils
import DpawsTools 
from DpawsTools._iorw import uchar2char as _uc2c, ushort2short as _us2s, double2double as _d2d
import random
import time


_conv = {np.dtype('uint8'):_uc2c, np.dtype('uint16'): _us2s}.get

sns.set(color_codes=True)

_fname = None
_fhandle = None
_data_width = None

def reset_reader():
  global _fname, _fhandle, _data_width
  if _fhandle:
    _fhandle.close()
  _fname = None
  _fhandle = None
  _data_width = None

def read_trace(filename, offset=0, samples=-1):
  global _fname, _fhandle, _data_width
  data_type = {
      8  : np.uint8,
      16 : np.uint16,
      32 : np.uint32,
      64 : np.float64,
      }

  if _fname != filename:
    reset_reader()
    _fname = filename
    _fhandle = open(_fname, 'rb')
    magic_number = struct.unpack('h', _fhandle.read(2))[0]
    sample_rate  = struct.unpack('f', _fhandle.read(4))[0]
    range_mv     = struct.unpack('i', _fhandle.read(4))[0]
    offset_mv    = struct.unpack('f', _fhandle.read(4))[0]
    data_width   = struct.unpack('B', _fhandle.read(1))[0]
    offset_file  = struct.unpack('i', _fhandle.read(4))[0]
    sub_version  = struct.unpack('B', _fhandle.read(1))[0]
    status_flag  = struct.unpack('B', _fhandle.read(1))[0]
    pad          = _fhandle.read(3)
    _data_width  = data_width

  start_pos = max(0, offset * _data_width // 8)
  _fhandle.seek(start_pos + 24, 0) # from the beginning

  return np.fromfile(_fhandle, data_type[_data_width], samples)

#Yuan: input the instest test samples
#test_samples = np.array([653, 40274, 41324])
test_samples = np.array([40274])
#------------------------------------------------------------------------#
# t-test
#------------------------------------------------------------------------#


#t_list = []
#x_axis = []
#for i in range(1, 100):
#    #print("reading boot trace-{}".format(i))
#    test_trace = i*100
#    trace = read_trace("Z:/boolean-masked-8-bit-aes-olimex/t-test-2019-07-15_16_43/ttest_t/t_ttest-{}.dwfm".format(test_trace))[test_sample]
#    #trace = read_trace("Z:/boolean-masked-8-bit-aes-olimex/t-test-2019-07-15_16_43/t_ttest-{}.dwfm".format(test_trace))[40274]
#    x_axis.append(test_trace)
#    t_list.append(abs(trace))

#plt.plot(x_axis,t_list)
#plt.axhline(y=4.5, color='r')
#plt.show()

#----------------------------------------------------------------------------------------------------#
# bootstrapping procedure
#----------------------------------------------------------------------------------------------------#
result_dir = "fn_evolution"
#bootstrapping number
bootnum = 200
numbers =[]
#boot on how many traces
#trace_num = 1000
x_axis = []
list_fix = []
list_rand = []
label_set=[]
trace_set=[]
p_final_list = []
plog_final_list = []
ks_p_evolution = []
bootlist = [400]
#binave = DpawsTools.Binave(test_sample, 1)
for bootnum in bootlist:
      print("working on {}boot".format(bootnum))
      for i in range(1, 21):
            trace_num = i*50
            x_axis.append(trace_num)
            print ("****************tracenumber:{}******".format(trace_num))
            for b in range(0,bootnum):
                rand_numbers = []
                dic_rand = {}
                binave = DpawsTools.Binave(len(test_samples), 1)
                #for i in range(0,trace_num-1):     
                #    #rand_numbers.append(random.choice(numbers))
                #    rand = random.randint(0, trace_num-1)
                #    #rand = i
                #    #rand_numbers.append(rand)
                #    if rand not in dic_rand:
                #        dic_rand[rand] = 1
                #    else:
                #        dic_rand[rand] = dic_rand[rand] + 1
                #rand_numbers = list(dic_rand.keys())
                #rand_numbers.sort()
                #print ("random_numbers:{}".format(rand_numbers))
                #print ("random_dic:{}".format(dic_rand))
                rand_readings = np.sort(np.random.randint(trace_num, size=trace_num))
                hist_readings = np.histogram(rand_readings, bins=trace_num)[0]
    
                with open('log.dwdb') as file:
                    for cnt, line in enumerate(file):
                        if cnt >= trace_num:
                            break

                        rcnt = hist_readings[cnt]
                        if rcnt < 1:
                          continue

                        line2 = dwdb_reader.parse_metadata_line(line)
                        trace = dwdb_reader.read_trace(line2['filename'])[test_samples]
                        trace = _conv(trace.dtype, _d2d)(trace)
                        label = line2['classifiers'].strip('{}')

                        binave.process([trace]*rcnt, [label]*rcnt)

                tt = next(binave.ttests())
                #print("tt:{}".format(tt))
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
                #print (t_p_log)
                p_final_list.append(t_p2[0])
            # append the final list
    
                #f_count.write("{}:{}\n".format(b, counter))
                #Dpaws.TraceWrite(tt, tracefile= result_dir_t+'/boot_t/t_ttest_boot-{}.dwfm'.format(b))
                #Dpaws.TraceWrite(t_p2, tracefile= result_dir_t+'/boot_p/p_ttest_boot-{}.dwfm'.format(b))
                #Dpaws.TraceWrite(t_p_log, tracefile= result_dir_t+'/boot_p_log/plog_ttest_boot-{}.dwfm'.format(b))
                #print("******FINISH BOOT" + str(b)+"*******") 

            np.savetxt('p_{}boot_{}traces.txt'.format(bootnum,trace_num),p_final_list,fmt = '%s', delimiter=',')
            #-------------------------------------------------------------------#
            # p_value distribution ploting
            #-------------------------------------------------------------------#
            #target_list = p_final_list
            ##min = np.amin(target_list)
            ##max = np.amax(target_list)
            #min = 0
            #max =1
            #bin_width = 0.01
            #bins_array = np.arange(min, max+bin_width, bin_width)
            ##plt.subplot(3,2,4)
            #plt.hist(target_list, bins=bins_array)
            #plt.title('p-fix vs random') 
            #plt.ylabel('frequency') 
            #plt.show()


            #----------------------------------------------------------------#
            # compare the uniform distribution with the p value distribution
            #----------------------------------------------------------------#

            step =  float(1)/bootnum
            _c = []
            value = 0
            for i in range(0,bootnum):
                _c.append(value)
                value = value + step
            c = np.array(_c)

            #target_list = c
            ##min = np.amin(target_list)
            ##max = np.amax(target_list)
            #min = 0
            #max =1
            #bin_width = 0.01
            #bins_array = np.arange(min, max+bin_width, bin_width)
            ##plt.subplot(3,2,4)
            #plt.hist(target_list, bins=bins_array)
            #plt.title('p-fix vs random') 
            #plt.ylabel('frequency') 
            #plt.show()

            d, p_ks = stats.ks_2samp(p_final_list, c)

            if p_ks > small_value:
                p_ks_final =  p_ks
            else:
                p_ks_final = small_value

            print("p_ks:{}" .format(p_ks_final))
            ks_p_evolution.append(p_ks_final)

      #print(ks_p_evolution)
      fig = plt.figure()
      _p_ks_finallist= np.array(ks_p_evolution)
      p_ks_finallist_log = -np.log10(_p_ks_finallist)
      #print(p_ks_finallist_log)
      np.savetxt(result_dir+'/ksplog_{}boot.txt'.format(bootnum),p_ks_finallist_log,fmt = '%s', delimiter=',')
      np.savetxt(result_dir+'/ksp_{}boot.txt'.format(bootnum),ks_p_evolution,fmt = '%s', delimiter=',')

      plt.plot(x_axis,p_ks_finallist_log)
      plt.axhline(y=6.3, color='r')

      fig.savefig(result_dir+'/evolution_{}boot.png'.format(bootnum))
      #plt.show()    
