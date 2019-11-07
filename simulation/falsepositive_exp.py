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
target_snr_db = 1
trace_num = 1000
fix_value = 5
offset = 1
#hamming weight counting function
def hw(x):
  return bin(x).count("1")

#result_dir = time.strftime("rr_{}traces_snr{}_f{}".format(trace_num,target_snr_db,fix_value) + "-%Y-%m-%d_%H_%M")
#os.mkdir(result_dir)
result_dir_tp = "TP_set"
os.mkdir(result_dir_tp)
result_dir_fp = "FP_set"
os.mkdir(result_dir_fp)

t = 0
counter = 0
counter2 = 0

#-----------------------------------------------------#
# readin fix set trace
#----------------------------------------------------#

F1 = open('fix_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
fix = np.array(file_split1, dtype = np.float32)

while 1:
          #----------------------------------------------#
          # generate a random list
          #----------------------------------------------#
          random_list = np.random.randint(256, size = trace_num)
          hw_randlist = []

          for i in range(0,len(random_list)):
              hw_randlist.append(int(hw(random_list[i])))

          x_volts_orig = np.array(hw_randlist)
          x_volts = x_volts_orig +  offset

          mean_noise = 0
          sigma_noise = math.sqrt(np.var(x_volts)/target_snr_db)
          noise_volts = np.random.normal(mean_noise, sigma_noise, len(x_volts))

          y_volts = x_volts + noise_volts
          rand1_noise = y_volts
          #print ("rand1:{}".format(rand1_noise[0:10]))
          #----------------------------------------------#
          # generate a compare random list
          #----------------------------------------------#
          random_list = np.random.randint(256, size = trace_num)
          hw_randlist = []

          for i in range(0,len(random_list)):
              hw_randlist.append(int(hw(random_list[i])))


          x_volts_orig = np.array(hw_randlist)
          x_volts = x_volts_orig +  offset

          # Calculate signal power and convert to dB 
          mean_noise = 0
          sigma_noise = math.sqrt(np.var(x_volts)/target_snr_db)
          noise_volts = np.random.normal(mean_noise, sigma_noise, len(x_volts))

          # Noise up the original signal
          y_volts = x_volts + noise_volts
          rand2_noise = y_volts
          #print ("rand2_noise:{}".format(rand2_noise[0:10]))

          t, p = stats.ttest_ind(rand1_noise,rand2_noise,equal_var = False)
          t2,p2 = stats.ttest_ind(rand1_noise,fix,equal_var = False)
          #generate true positive case with small t value
          if abs(t2) > 4.5 and abs(t2) < 6:
              counter2 = counter2 + 1
              print("find tp {}".format(counter2))
              #np.savetxt(result_dir+'/{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
              #np.savetxt(result_dir+'/{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')
              np.savetxt(result_dir_tp+'/{}tp_{}traces_{}SNR_f{}.txt'.format(counter, trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
           
          #print(t)
          #generate false positive case
          if abs(t) > 4.5:
              counter = counter + 1
              print("find fp {}".format(counter))
              #np.savetxt(result_dir+'/{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
              #np.savetxt(result_dir+'/{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(abs(t), trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')
              np.savetxt(result_dir_fp+'/{}Rand1Noise_{}traces_{}SNR_f{}.txt'.format(counter, trace_num,target_snr_db,fix_value),rand1_noise,fmt = '%s', delimiter=',')
              np.savetxt(result_dir_fp+'/{}Rand2Noise_{}traces_{}SNR_f{}.txt'.format(counter, trace_num,target_snr_db,fix_value),rand2_noise,fmt = '%s', delimiter=',')