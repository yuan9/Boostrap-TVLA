
from __future__ import absolute_import, division, print_function, with_statement

import os
import sys
import time
import math

import numpy as np
from scipy.stats import distributions
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

from os import urandom as _rand

target_snr_db = 1
trace_num = 1000
fix_value = 5
offset = 1

#hamming weight counting function
def hw(x):
  return bin(x).count("1")

def bytes2hw(arr, size=8):
  return np.sum((np.frombuffer(arr, dtype=np.uint8) - ord('0')).reshape(-1, size), axis=1, dtype=np.float64)


#result_dir = time.strftime("rr_{}traces_snr{}_f{}".format(trace_num,target_snr_db,fix_value) + "-%Y-%m-%d_%H_%M")
# os.mkdir(result_dir)
result_dir_tp = "TP_set"
result_dir_fp = "FP_set"
if not os.path.exists(result_dir_tp): os.mkdir(result_dir_tp)
if not os.path.exists(result_dir_fp): os.mkdir(result_dir_fp)

script_no = sys.argv[1]

t = 0
counter = 0
counter2 = 0

mean_hw = np.array([4]*trace_num)

while True:
  #----------------------------------------------#
  # generate two random list
  #----------------------------------------------#
  both_rands = np.array([hw(ord(r)) for r in _rand(trace_num*2)]).reshape(2, -1)

  #----------------------------------------------#
  # generate a random list
  #----------------------------------------------#
  hw_randlist = both_rands[0]

  x_volts_orig = hw_randlist
  x_volts = x_volts_orig + offset

  mean_noise = 0
  sigma_noise = math.sqrt(np.var(x_volts)/target_snr_db)
  noise_volts = np.random.normal(mean_noise, sigma_noise, len(x_volts))

  y_volts = x_volts + noise_volts
  rand1_noise = y_volts
  # print ("rand1_noise:{}".format(rand1_noise[0:10]))

  #----------------------------------------------#
  # generate a random list
  #----------------------------------------------#
  hw_randlist = both_rands[1]

  x_volts_orig = hw_randlist
  x_volts = x_volts_orig + offset

  # Calculate signal power and convert to dB
  mean_noise = 0
  sigma_noise = math.sqrt(np.var(x_volts)/target_snr_db)
  noise_volts = np.random.normal(mean_noise, sigma_noise, len(x_volts))

  # Noise up the original signal
  y_volts = x_volts + noise_volts
  rand2_noise = y_volts
  # print ("rand2_noise:{}".format(rand2_noise[0:10]))

  #----------------------------------------------#
  # generate a fixed list
  #----------------------------------------------#
  hw_randlist = mean_hw

  x_volts_orig = hw_randlist
  x_volts = x_volts_orig + offset

  # Calculate signal power and convert to dB
  mean_noise = 0
  sigma_noise = math.sqrt(np.var(x_volts)/target_snr_db)
  noise_volts = np.random.normal(mean_noise, sigma_noise, len(x_volts))

  # Noise up the original signal
  y_volts = x_volts + noise_volts
  fix = y_volts

  t,  p  = stats.ttest_ind(rand1_noise, rand2_noise, equal_var = False)
  t2, p2 = stats.ttest_ind(rand1_noise, fix,         equal_var = False)

  #generate true positive case with small t value
  if abs(t2) > 5 and abs(t2) < 7 and counter2 < counter:
    counter2 = counter2 + 1
    print("find tp {}".format(counter2))
    #np.savetxt(result_dir+'/{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
    #np.savetxt(result_dir+'/{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')
    np.savetxt(result_dir_tp+'/{}-{}tp_{}traces_{}SNR_f{}.txt'.format(counter, script_no, trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
    np.savetxt(result_dir_tp+'/{}-{}fix_{}traces_{}SNR_f{}.txt'.format(counter, script_no, trace_num,target_snr_db,fix_value),fix,fmt = '%s', delimiter=',')

  #generate false positive case
  if abs(t) > 5:
    counter = counter + 1
    print("find fp {}".format(counter))
    #np.savetxt(result_dir+'/{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
    #np.savetxt(result_dir+'/{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')
    np.savetxt(result_dir_fp+'/{}-{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(counter, script_no, trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
    np.savetxt(result_dir_fp+'/{}-{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(counter, script_no, trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')

  #print('.', end='')

