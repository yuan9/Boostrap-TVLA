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


#----------------------------------------------------------------------------------------------------#
# bootstrapping procedure
#----------------------------------------------------------------------------------------------------#
result_dir = "Boot_FullTrace2"
if not os.path.exists(result_dir):
  os.mkdir(result_dir)

#Yuan: Note that the basic range is from (40,180)
#sample_start = 40 + 83
#sample_end = 40 +84
#---------------------------------------#
# important parameters
#----------------------------------------#
sample_start = 40
sample_end = 180
bootnum = 100
trace_num = 1000
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

ks_p_list=[]
ks_p_list_log = []
small_value =  1.8e-305
#binave = dpawstools.binave(test_sample, 1)
for sample_start in range (sample_start, sample_end) :
#for sample_start in range (40,43) :
      print("working on sample-{}".format(sample_start))
      #------------------------------------------#
      # trace reading:
      #------------------------------------------#
      dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/RawTraces_new.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/hw-AES-Protected/')
      data_batch, meta_batch = dsr.read_batch(trace_num, sample_start, sample_start + 1)
      data_np = np.asarray(data_batch)
      #print(data_batch)
      data_trans = data_np.T[0]
      data_trans.astype(int)
      #print(data_trans)
      #processing of classifiers
      classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('s=')]
      classifiers= np.asarray(classifiers)
      #print(classifiers)
      #------------------------------------------#
      # Boostrapping procedure
      #------------------------------------------#
      p_list = []
      for b in range(0,bootnum):
          fix_list = []
          rand_list= []

          random_list = np.random.randint(len(data_trans)-1, size = len(data_trans))
          random_list.sort()
          #print(random_list)
          for rand in random_list:
              #print(data_trans[rand])
              #print(type(data_trans[rand])) 
              if classifiers[rand] == '0':
                    fix_list.append(data_trans[rand])
              if classifiers[rand] == '1':
                    rand_list.append(data_trans[rand])
          #print("fix_list:{}".format(fix_list))
          #print("rand_list:{}".format(rand_list))   
          t, p = stats.ttest_ind(rand_list, fix_list, equal_var = False)
          # generate the p_list for each sample
          p_list.append(max(p,small_value))
      #print("p_list:{}".format(p_list))
      #-------------------------------------------#
      # 1-sample ks-test
      #-------------------------------------------#
      # calculate the 1-sample ks-test value
      # for each sample calculate the value
      d, p_ks = stats.kstest(p_list, 'uniform')
      if p_ks > small_value:
          p_ks_final =  p_ks
      else:
          p_ks_final = small_value

      #print("p_ks:{}" .format(p_ks_final))

      p_final_list.append(p_ks_final)

#print("p_final_list:{}".format(p_final_list))
_ks_p_list= np.array(p_final_list)
ks_p_list_log = -np.log10(_ks_p_list)
#print("ks_p_list_log:{}".format(ks_p_list_log))
np.savetxt(result_dir+'/ksplog_{}traces_{}boot.txt'.format(trace_num,bootnum),ks_p_list_log,fmt = '%s', delimiter=',')

font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'

plt.xlabel('Time');
plt.ylabel('-log10(p-value)');

plt.plot(ks_p_list_log,linewidth=2, linestyle='-',  color = 'navy')
plt.axhline(y=5.3, color='r', linewidth=2)
#plt.ylim(top = 10 )


plt.show()
