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

#import aes_internals as aise
import dwdb_reader
 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import time
import util.dwdb_reader as io
import util.tests as tests

#---------------------------------------------------------#
# packages when use dpaws tools
#--------------------------------------------------------#

#import Dpaws
#import DpawsUtils
#import DpawsTools 
#from DpawsTools._iorw import uchar2char as _uc2c, ushort2short as _us2s, double2double as _d2d
#import Dpaws


#_conv = {np.dtype('uint8'):_uc2c, np.dtype('uint16'): _us2s}.get
#test_samples = np.array([40274])
#---------------------------------------------------------#
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
#test_samples = np.array([196])

#------------------------------------------------------------------------#
# t-test
#------------------------------------------------------------------------#


#t_list = []
#x_axis = []
#for i in range(1, 11):
#    print("reading boot trace-{}".format(i))
#    test_trace = i*100
#    trace = read_trace("Z:/aquisition_AESDpad_unprotected/data/t-trace/v000_{}_t1.dwfm".format(test_trace))[196]
#    x_axis.append(test_trace)
#    t_list.append(abs(trace))

#plt.plot(x_axis,t_list)
#plt.axhline(y=4.5, color='r')
#plt.show()

#trace = read_trace("Z:/aquisition_AESDpad_unprotected/data/t-trace/v000_100_t1.dwfm")
#plt.plot(trace)
#trace3 = read_trace("Z:/aquisition_AESDpad_unprotected/data/t-trace/v000_500_t1.dwfm")
#plt.plot(trace3)
#trace2 = read_trace("Z:/aquisition_AESDpad_unprotected/data/t-trace/v000_1000_t1.dwfm")
#plt.plot(trace2)
#plt.axhline(y=4.5, color='r')
#plt.axvline(x=196, color='g')
#plt.show()
#----------------------------------------------------------------------------------------------------#
# bootstrapping procedure
#----------------------------------------------------------------------------------------------------#
result_dir = "fn_Bootevolution_1sample"
if not os.path.exists(result_dir):
  os.mkdir(result_dir)
  os.mkdir(result_dir+'/boot-p')

#Yuan: Note that the basic range is from (40,180)
sample_start = 40 + 83
sample_end = 40 +84
bootlist = [300]
trace_range = 500
step = 20
#bootstrapping number
#bootnum = 200
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

#binave = dpawstools.binave(test_sample, 1)
for bootnum in bootlist:
      print("working on {}boot".format(bootnum))
      p_final_list = []
      plog_final_list = []
      ks_p_evolution = []
      for i in range(1, int(trace_range/step)+1):
            trace_num = i*step
            x_axis.append(trace_num)
            print ("****************tracenumber:{}******".format(trace_num))
            for b in range(0,bootnum):
                rand_numbers = []
                dic_rand = {}
                #binave = dpawstools.binave(len(test_samples), 1)
                #binave = DpawsTools.Binave(len(test_samples), 1)
                rand_readings = np.sort(np.random.randint(trace_num, size=trace_num))
                hist_readings = np.histogram(rand_readings, bins=trace_num)[0]
                
                # # creat reader
                # dsr = io.dwdb_reader('log.dwdb')
                # # [196,197) this is from...to...sample, data_batch is a list of numpy array, this specify the single sample
                # data_batch, meta_batch = dsr.read_batch(trace_num, 40274, 40275)

                # data_np = np.asarray(data_batch) # 2D numpy array of sample

                # trace reading:
                dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/RawTraces_new.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/')
                data_batch, meta_batch = dsr.read_batch(trace_num, sample_start, sample_end)
                data_np = np.asarray(data_batch)

                #processing of classifiers
                classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('s=')]
                classifiers= np.asarray(classifiers) # 2D numpy array of classifier
                #print("finish readin traces")
                #processing of classifiers
                # classifiers = [m['classifiers'].strip('{}') for m in meta_batch]
                # classifiers = np.asarray(classifiers) # 2D numpy array of classifier

                data = np.ones_like(data_np[0])
                data_label = np.ones_like(classifiers[0])
                #i= bins, cnt = frequency of bin
                for i, cnt in enumerate(hist_readings):
                        if cnt < 1:
                          continue 
                        d = np.repeat(data_np[i], cnt).reshape(-1, cnt).T
                        data = np.vstack((data, d))
                        c = np.repeat(classifiers[i], cnt).reshape(-1, cnt).T
                        data_label = np.vstack((data_label, c))

                data = data[1:,:]
                data_label = data_label[1:,:]
                tt2 = tests.welch_ttest_fvr(data, data_label)[np.newaxis]
                #print("tt2:{}".format(tt2))
                #--------------------------------------------------------------#
                #binave = DpawsTools.Binave(len(test_samples), 1)
                #with open('log.dwdb') as file:
                #    for cnt, line in enumerate(file):
                #        if cnt >= trace_num:
                #            break

                #        rcnt = hist_readings[cnt]
                #        if rcnt < 1:
                #          continue

                #        line2 = dwdb_reader.parse_metadata_line(line)
                #        trace = dwdb_reader.read_trace(line2['filename'])[test_samples]
                #        trace = _conv(trace.dtype, _d2d)(trace)
                #        label = line2['classifiers'].strip('{}')

                #        binave.process([trace]*rcnt, [label]*rcnt)

                #tt = next(binave.ttests())
                #print("tt:{}".format(tt))
                #--------------------------------------------------------------#
                #print("tt:{}".format(tt))
                t_abs = np.absolute(tt2)
                t_p = 2*(1- norm.cdf(t_abs))
                #post processing
                small_value =  1e-323
                t_p[np.where(np.isnan(t_p))] = small_value
                t_p[np.where(t_p < small_value)] = small_value
                #t_p_log = -np.log10(t_p)
                #print (t_p_log)
                p_final_list.append(t_p[0])
            # append the final list
    
                #f_count.write("{}:{}\n".format(b, counter))
                #dpaws.tracewrite(tt, tracefile= result_dir_t+'/boot_t/t_ttest_boot-{}.dwfm'.format(b))
                #dpaws.tracewrite(t_p2, tracefile= result_dir_t+'/boot_p/p_ttest_boot-{}.dwfm'.format(b))
                #dpaws.tracewrite(t_p_log, tracefile= result_dir_t+'/boot_p_log/plog_ttest_boot-{}.dwfm'.format(b))
                #print("******finish boot" + str(b)+"*******") 

            np.savetxt(result_dir+'/boot-p/p_{}boot_{}traces.txt'.format(bootnum,trace_num),p_final_list,fmt = '%s', delimiter=',')
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
            d, p_ks = stats.kstest(p_final_list, 'uniform')


            if p_ks < small_value:
                p_ks = small_value

            print("p_ks:{}" .format(p_ks))
            ks_p_evolution.append(p_ks)

      #print(ks_p_evolution)
      fig = plt.figure()
      _p_ks_finallist= np.array(ks_p_evolution)
      p_ks_finallist_log = -np.log10(_p_ks_finallist)
      #print(p_ks_finallist_log)
      np.savetxt(result_dir+'/ksplog_{}boot.txt'.format(bootnum),p_ks_finallist_log,fmt = '%s', delimiter=',')
      np.savetxt(result_dir+'/ksp_{}boot.txt'.format(bootnum),ks_p_evolution,fmt = '%s', delimiter=',')

      plt.plot(x_axis,p_ks_finallist_log)
      plt.axhline(y=5, color='r')

      fig.savefig(result_dir+'/evolution_{}boot.png'.format(bootnum))
      #plt.show()    
