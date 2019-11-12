import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import sys
import math
from scipy import stats
import time
import os

a=sys.argv
target_snr_db = 0.01
trace_num = 1000
fix_value = 5
offset = 1
#hamming weight counting function
def hw(x):
  return bin(x).count("1")

#result_dir = time.strftime("rr_{}traces_snr{}_f{}".format(trace_num,target_snr_db,fix_value) + "-%Y-%m-%d_%H_%M")
#os.mkdir(result_dir)
result_dir_tp = "TP_SmallValue_set"
#os.mkdir(result_dir_tp)

t = 0
counter = 0
counter2 = 0

if not os.path.exists(result_dir_tp):
    os.mkdir(result_dir_tp)
    #os.mkdir(result_dir+'/boot-p')


while 1:
#---------------------------------------------------------@
# Random Set 
#---------------------------------------------------------#
          #----------------------------------------------#
          # generate a random list
          #----------------------------------------------#
          random_list = np.random.randint(256, size = trace_num)
          hw_randlist = []

          for i in range(0,len(random_list)):
              hw_randlist.append(int(hw(random_list[i])))

          x_volts_orig = np.array(hw_randlist)
          x_volts = x_volts_orig +  offset
          np.savetxt(result_dir_tp+'/sig_orig.txt',x_volts,fmt = '%u', delimiter=',')

          x_watts = x_volts ** 2
          x_db = 10 * np.log10(x_watts)

          #-----------------------------------------------#
          # adding noise using target SNR
          #-----------------------------------------------#
          # Set a target SNR 

          # Calculate signal power and convert to dB 
          sig_avg_watts = np.mean(x_watts) 
          sig_avg_db = 10 * np.log10(sig_avg_watts)
          # Calculate noise according to [2] then convert to watts
          noise_avg_db = sig_avg_db - target_snr_db 
          noise_avg_watts = 10 ** (noise_avg_db / 10)
          # Generate an sample of white noise
          mean_noise = 0
          noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))
          #print("noise:{}".format(noise_volts))
          # Noise up the original signal
          y_volts_rand = x_volts + noise_volts
#---------------------------------------------------------@
# fix Set 
#---------------------------------------------------------#

          x_volts_fix = np.empty(trace_num)
          x_volts_fix.fill(fix_value + offset)
          x_volts_fix.astype(int)
          #print("fix value:{}".format(x_volts_fix))

          x_watts_fix = x_volts_fix ** 2
          x_db_fix = 10 * np.log10(x_watts_fix)
          sig_avg_watts_fix = np.mean(x_watts_fix) 
          sig_avg_db_fix = 10 * np.log10(sig_avg_watts_fix)
          # Calculate noise according to [2] then convert to watts
          noise_avg_db_fix = sig_avg_db_fix - target_snr_db
          noise_avg_watts_fix = 10 ** (noise_avg_db_fix / 10)
          # Generate an sample of white noise
          noise_volts_fix = np.random.normal(mean_noise, np.sqrt(noise_avg_watts_fix), len(x_watts_fix))

          y_volts_fix = x_volts_fix + noise_volts_fix

#---------------------------------------------------------@
# t-test 
#---------------------------------------------------------#
          t, p = stats.ttest_ind(y_volts_rand,y_volts_fix,equal_var = False)

          #generate false positive case
          if abs(t) > 4.5 and abs(t) < 6:
              counter = counter + 1
              print("find tp {}:{}".format(counter,abs(t)))
              #np.savetxt(result_dir+'/{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
              #np.savetxt(result_dir+'/{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')
              np.savetxt(result_dir_tp+'/{}-{}RandNoise_{}traces_{}SNR_f{}.txt'.format(counter,t, trace_num,target_snr_db,fix_value),y_volts_rand,fmt = '%s', delimiter=',')
              np.savetxt(result_dir_tp+'/{}-{}FixNoise_{}traces_{}SNR_f{}.txt'.format(counter,t, trace_num,target_snr_db,fix_value),y_volts_fix,fmt = '%s', delimiter=',')
