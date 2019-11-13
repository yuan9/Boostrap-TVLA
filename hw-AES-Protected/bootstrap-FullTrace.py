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
result_dir = "Boot_FullTrace"
if not os.path.exists(result_dir):
  os.mkdir(result_dir)

#Yuan: Note that the basic range is from (40,180)
#sample_start = 40 + 83
#sample_end = 40 +84
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
bootnum = 100
trace_num = 1000
ks_p_list=[]
#binave = dpawstools.binave(test_sample, 1)
for sample_start in range (40, 180) :
      print("working on sample-{}".format(sample_start))
      p_final_list = []
      plog_final_list = []
      ks_p_evolution = []

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
          dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/RawTraces.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/')
          data_batch, meta_batch = dsr.read_batch(trace_num, sample_start, sample_start + 1)
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

          t_abs = np.absolute(tt2)
          t_p = 2*(1- norm.cdf(t_abs))
          #print(t_p)
          #post processing
          small_value =  1.8e-305
          t_p[np.where(np.isnan(t_p))] = small_value
          t_p[np.where(t_p < small_value)] = small_value
          #t_p_log = -np.log10(t_p)
          #print (t_p_log)
          p_final_list.append(t_p[0])
          
        # --------------------------------------------------------
        # 1-sample ks test
        #---------------------------------------------------------
      #print (p_final_list)
      d, p_ks = stats.kstest(p_final_list, 'uniform')
      ks_p_list.append(p_ks)

      _ks_p_list= np.array(ks_p_list)
      ks_p_list_log = -np.log10(_ks_p_list)

np.savetxt(result_dir+'/ksplog_{}traces_{}boot.txt'.format(trace_num,bootnum),ks_p_list_log,fmt = '%s', delimiter=',')

font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'

plt.xlabel('Time');
plt.ylabel('-log10(p-value)');

print(ks_p_list_log)
plt.plot(ks_p_list_log,linewidth=2, linestyle='-',  color = 'navy')
plt.axhline(y=5.3, color='r', linewidth=2)
#plt.ylim(top = 10 )
# plt.plot(t_evolution[0])
# plt.plot(t_evolution[1])
# plt.plot(t_evolution[2])
# plt.axhline(y=4.5, color='r')
# plt.axvline(x=83,  color='b')
# #plt.legend(['10000','20000', '30000'], loc='upper left')
# plt.legend(legend, loc='upper left')


plt.show()