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
result_dir = "Boot_FullTrace_test"
if not os.path.exists(result_dir):
  os.mkdir(result_dir)

#Yuan: Note that the basic range is from (40,180)
sample_start = 40 
sample_end = 180
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
test_trace = 100

# read in traces 
dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/RawTraces.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/')
data_batch, meta_batch = dsr.read_batch(trace_num, sample_start, sample_end)
data_np = np.asarray(data_batch)

#processing of classifiers
classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('s=')]
classifiers= np.asarray(classifiers) # 2D numpy array of classifier
#print(classifiers)
for i in range(0, len(data_np)):
#for i in range(0, 4):
    if classifiers[i] == '1':
        list_rand.append(data_np[i])
    if classifiers[i] == '0': 
        list_fix.append(data_np[i])

print("list_rand:{}".format(len(list_rand)))
print("list_fix:{}".format(len(list_fix)))

rand_np = np.asarray(list_rand)
rand_trans =  rand_np.T
#print (rand_trans)


fix_np = np.asarray(list_fix)
fix_trans =  fix_np.T
print("rand:{}".format(len(rand_trans)))
print("fix:{}".format(len(fix_trans)))

p_list = []
small_value = 1e-323
p_ks_finallist = []
for s in range(0,sample_end - sample_start +1):
    for b in range(0, bootnum):
        boot_rand = []
        boot_fix = []
        random_list_rand = np.random.randint(len(list_rand), size = len(list_rand))
        random_list_fix = np.random.randint(len(list_fix), size = len(list_fix))

        for i in random_list_rand:
                boot_rand.append(rand_trans[i])

        for i in random_list_fix:
                boot_fix.append(fix_trans[i])

        t, p = stats.ttest_ind(rand_trans[i], fix_trans[i], equal_var = False)
        p_list.append(max(p,small_value))

        d, p_ks = stats.kstest(p_list, 'uniform')


        if p_ks > small_value:
            p_ks_final =  p_ks
        else:
            p_ks_final = small_value

        print("p_ks:{}" .format(p_ks_final))


    p_ks_finallist.append(p_ks_final)
    _ks_p_list= np.array(p_ks_finallist)
    ks_p_list_log = -np.log10(_ks_p_list)

np.savetxt(result_dir+'/ksplog_{}boot.txt'.format(bootnum),p_ks_finallist_log,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/ksp_{}boot.txt'.format(bootnum),p_ks_finallist,fmt = '%s', delimiter=',')

plt.plot(x_axis2,p_ks_finallist_log)
plt.axhline(y=5.3, color='r')

fig.savefig(result_dir+'/evolution_{}boot.png'.format(bootnum))
plt.show()
