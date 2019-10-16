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


meta = {}
result_dir_t = time.strftime("bootstrapping_ResultAnalysis" + "-%Y-%m-%d_%H_%M")
#result_dir_s = "boot10000_TestPoint_Distribution_SmallPeakNoLeak1000-noLeak100000"
result_dir_s = "boot10000_sample-40274"
#result_dir_s = "debug_folder"
#p_obsv = Dpaws.TraceRead('Z:/boolean-masked-8-bit-aes-olimex/bootstrapping-40000-45000-2019-07-17_16_00/p_ttest-obsr.dwfm', metadata=meta)
#p_obsv = Dpaws.TraceRead('Z:/boolean-masked-8-bit-aes-olimex/t-test-2019-07-15_16_43/ttest_p_log/plog_ttest-1000.dwfm', metadata=meta)
p_obsv_log =read_trace('Z:/boolean-masked-8-bit-aes-olimex/t-test-2019-07-15_16_43/ttest_p_log/plog_ttest-1000.dwfm')[40000:45000]
#print("p_obsv length:"+str(len(p_obsv)))
#p_obsv2 = p_obsv[40000:45000]
Dpaws.TraceWrite(p_obsv_log, tracefile= result_dir_t+'/obsrv_test_1000.dwfm')

p_obsv_log2 =read_trace('Z:/boolean-masked-8-bit-aes-olimex/t-test-2019-07-15_16_43/ttest_p_log/plog_ttest-5000.dwfm')[40000:45000]
#print("p_obsv length:"+str(len(p_obsv)))
#p_obsv2 = p_obsv[40000:45000]
Dpaws.TraceWrite(p_obsv_log2, tracefile= result_dir_t+'/obsrv_test_5000.dwfm')

#p_obsv_log =  Dpaws.TraceRead('Z:/boolean-masked-8-bit-aes-olimex/bootstrapping-40000-45000-2019-07-17_16_00/p_ttest-obsr-log.dwfm', metadata=meta)


bootnum = 10000
X = []
for i in range(0, bootnum):
    print("reading boot trace-{}".format(i))
    trace = read_trace("Z:/boolean-masked-8-bit-aes-olimex/bootstrapping1000-sample40000-45000-2019-07-17_18_07/boot_p/p_ttest_boot-{}.dwfm".format(i))
    X.append(trace)
print("X length:")
print (len(X))
    
#Yuan: transpose the original array.
X_np = np.array(X)
X_np_trans = np.transpose(X_np)
X_np_trans_log = -np.log10(X_np_trans)

##--------------------------------------------------------------------------------------#
## Hypothesis test for each value
##--------------------------------------------------------------------------------------#
## len(meta) is the boot repeating time
#p_boot_hypo = []
#for i in range(0,len(p_obsv)):
#    counter = 0
#    for j in range(0,len(X_np_trans[0])):
#        if X_np_trans[i][j] > p_obsv[i]:
#            counter =  counter + 1
#    #p = counter/len(meta)
#    p = counter/len(X)
#    p_boot_hypo.append(p)
##print (p_boot_hypo)
#tr = np.array(p_boot_hypo)
#p_boot_hypo2 = []

#small_value = 1e-323
#for i in range(0, len(p_boot_hypo)):
#    if p_boot_hypo[i] > small_value:
#          p_boot_hypo2.append(p_boot_hypo[i])
#    else:
#          p_boot_hypo2.append(small_value)
#tr_log = -np.log10(p_boot_hypo2)
##print("tr:")
##print(tr)
#Dpaws.TraceWrite(tr, tracefile=result_dir_t+'/p_boot_hypo.dwfm')
#Dpaws.TraceWrite(tr_log, tracefile=result_dir_t+'/p_log_boot_hypo.dwfm')
##p_boot_hypo_log = -np.log10(p_boot_hypo)

##---------------------------------------------------------------------------------------#
## Calculate the percentile
##---------------------------------------------------------------------------------------#
percent = 99
percentil_high = []
percentil_low = []
small_value = 1e-323
percentil_high_2 = []
percentil_low_2 = []

percentil_high = np.percentile(X_np_trans, percent, axis = 1)

for i in range(0, len(percentil_high)):
      if percentil_high[i] > small_value:
            percentil_high_2.append(percentil_high[i])
      else:
            percentil_high_2.append(small_value)

Dpaws.TraceWrite(percentil_high_2, tracefile= result_dir_t+'/p_BootPentile_high.dwfm')

percentil_high_log = -np.log10(percentil_high_2)
#print("percentil_high_log:")
#print(percentil_high_log[test_point])
Dpaws.TraceWrite(percentil_high_log, tracefile=result_dir_t+'/p_BootPentile_high_log.dwfm')

percentil_low = np.percentile(X_np_trans, (100-percent), axis = 1)

for i in range(0, len(percentil_low)):
      if percentil_low[i] > small_value:
            percentil_low_2.append(percentil_low[i])
      else:
            percentil_low_2.append(small_value)
print("percentil_low:")
#print(percentil_low[test_point])    
Dpaws.TraceWrite(percentil_low_2, tracefile=result_dir_t+'/p_BootPentile_low.dwfm')



percentil_low_log = -np.log10(percentil_low_2)
print("percentil_low_log:")
#print(percentil_low_log[test_point])
Dpaws.TraceWrite(percentil_low_log, tracefile=result_dir_t+'/p_BootPentile_low_log.dwfm') 
  


#--------------------------------------------------------------------------------------#
# Result Ploting
#--------------------------------------------------------------------------------------#
bin_num = 100
base = 40000
#test_point = 126

#raw_input()
#with leakage
#test_sample_array = [1126,1130,1336,1537,1628,1632,1736,1740,1849,1994,2039,2309,2339,2377,2387,2391,2401,2404,2441,2445,2455,2458,2465,2475,2482,2485,2499]
#test_sample_array = [40274,40749,42458,42607,42689,44137,44208,44371,44724,42699,42716,42744,42804,43042,43052,44167,44235,44493,43082,43160,43516,43693,43720,43726,44191,44276,44642]
test_sample_array = [40274]
#wihout leakage
#test_sample_array =[1346,1370,1160,1547,1561,1588,1621,1715,1812,2224,2286] 
#test_sample_array =[42160,42240,42280,42300,42350,42000,41865,41880,41890,41670,41695,41805,41825,41830,41815,41825,41835,41900]
#leakage already
#test_sample_array =[274,749,2458,2587,2607,2689,2699,2716,2744,2804,2824]
#-----------------------------------------------------------#
# small no leak peak in 1000, but even lower peak in 100000
#test_sample_array = [42197,42228,42233,42277,42265,41183,41200,41170,42024]
#------------------------------------------------------------#
#plt.figure()
test_sample_np = np.array(test_sample_array) - base
test_sample_np.astype(int)
print (test_sample_np)
for test_point in test_sample_np:
      print("-------------testing sample-{}:".format(test_point))
      print("p-value:")
      print (np.amax(X_np_trans[test_point]))
      print (np.amin(X_np_trans[test_point]))
      bin_width = (np.amax(X_np_trans[test_point]) - np.amin(X_np_trans[test_point]))/bin_num
      bins_array = np.arange(np.amin(X_np_trans[test_point]),np.amax(X_np_trans[test_point])+bin_width,bin_width)

      fig1 = plt.figure()
      plt.hist(X_np_trans[test_point], bins=bins_array)
      plt.title('p_value')
      fig1.savefig(result_dir_s+'/dis_p_sample-'+str(test_point)+'.png')
      #plt.draw()

      #plt.figure()
      print("p-value-log:")
      print (np.amax(X_np_trans_log[test_point]))
      print (np.amin(X_np_trans_log[test_point]))
      bin_width = (np.amax(X_np_trans_log[test_point]) - np.amin(X_np_trans_log[test_point]))/bin_num
      bins_array = np.arange(np.amin(X_np_trans_log[test_point]),np.amax(X_np_trans_log[test_point])+bin_width,bin_width)
      #bin_width = 25/bin_num
      #bins_array = np.arange(0,(25+bin_width),bin_width)

      fig2 = plt.figure()
      plt.hist(X_np_trans_log[test_point], bins=bins_array)
      plt.title('p_log')
      fig2.savefig(result_dir_s+'/dis_p_log_sample-'+str(test_point)+'.png')

fig3 = plt.figure()
plt.plot(percentil_low_log,'g',percentil_high_log,'r',p_obsv_log,'b')
plt.title('boot_percentil')
fig3.savefig(result_dir_s+'/percentil.png')


plt.show()