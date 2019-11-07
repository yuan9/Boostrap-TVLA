import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from scipy import stats
from scipy.stats import chi2
import random
import array
import os
import time
import sys
import decimal

target_snr_db = 1
bootnum = 600
fix_value = 5
result_dir = "fp_ml_fp"
#os.mkdir(result_dir)
filenum = 900
for m in range(1, filenum):
        print("working on set-{}".format(m))
        #----------------------------------------------------------#
        # Read in the random set
        #----------------------------------------------------------#
        rand = []
        fix = []
        #F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.01631976779Rand1Noise_1000traces_1SNR_f5.txt','r')
        #F1 = open('Z:/simulation-trace/TP_SmallValue_set/666FixNoise_1000traces_0.01SNR_f5.txt','r')
        #F1 = open('rand_noise.txt','r')
        F1 = open('Z:/simulation-trace/FP_set/{}Rand1Noise_1000traces_1SNR_f5.txt'.format(m),'r')
        file_string1 = F1.read()
        F1.close()
        file_split1 = file_string1.split("\n")[:-1]
        #print(file_split1)
        rand = np.array(file_split1, dtype = np.float32)

        #----------------------------------------------------------#
        # Read in the rand comparison set
        #----------------------------------------------------------#
        rand2 = []
        #F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.01631976779Rand2Noise_1000traces_1SNR_f5.txt','r')
        #F1 = open('Z:/simulation-trace/TP_SmallValue_set/666RandNoise_1000traces_0.01SNR_f5.txt','r')
        #F1 = open('fix_noise.txt','r')
        F1 = open('Z:/simulation-trace/FP_set/{}Rand2Noise_1000traces_1SNR_f5.txt'.format(m),'r')
        file_string1 = F1.read()
        F1.close()
        file_split1 = file_string1.split("\n")[:-1]
        #print(file_split1)
        rand2 = np.array(file_split1, dtype = np.float32)

        #-------------------------------------------------------------#
        # t-test
        #--------------------------------------------------------------#
        t_list = []
        x_axis = []
        #for i in range(1,100):
        #    test_trace = i * 100      
        #    t_obs2, p_obs2 = stats.ttest_ind(rand[0:test_trace-1],rand2[0:test_trace-1], equal_var = False)
        #    t_list.append(abs(t_obs2))
        #    x_axis.append(test_trace)
        t_obs, p_obs = stats.ttest_ind(rand,rand2, equal_var = False)
        print("obsv rand vs rand-t:{} p:{}".format(t_obs,p_obs))
        #plt.plot(x_axis,t_list)
        #plt.axhline(y=4.5, color='r')
        #plt.show()

        #---------------------------------------------------------------------#
        # Bootstrapping evlolution
        #---------------------------------------------------------------------#

        small_value = 1e-323 
        x_axis2 = []
        p_ks_finallist = []
        slice = 100
        imax =  len(rand)/slice
        #print(len(rand))
        #print(imax)

        #for i in range(0,1):
        for i in range(0,imax):
              test_trace = i * slice
              t_list = []
              p_list = []
              t_obs2, p_obs2 = stats.ttest_ind(rand[test_trace:test_trace+slice],rand2[test_trace:test_trace+slice], equal_var = False)
              x_axis2.append(test_trace)
              #print("{}-{}slice: t{}".format(test_trace,test_trace+slice, abs(t_obs2)))
              for b in range(0, bootnum):
                  random_list = np.random.randint(2*slice-1, size = 2*slice)
                  boot_rand = []
                  boot_rand2 = []
                  #print("random_list:{}".format(random_list))
                  for k in random_list:
                      r = random.randint(0,1)
                      #print("r:{}".format(r))
                      if r == 0:
                          boot_rand.append((rand[test_trace:test_trace+slice])[k%slice])
                      if r == 1:
                          boot_rand2.append((rand2[test_trace:test_trace+slice])[k%slice])
                  #print("boot_rand:{}".format(boot_rand))
                  #print("boot_rand2:{}".format(boot_rand2))
                  t_boot, p_boot = stats.ttest_ind(boot_rand,boot_rand2,  equal_var = False)
                  #print("p_list:{}".format(p_boot))
                  t_list.append(t_boot)
                  p_list.append(max(p_boot,small_value))
          

              step =  float(1)/slice
              _c = []
              value = 0
              for i in range(0,slice):
                  _c.append(value)
                  value = value + step
              c = np.array(_c)
              #print("c:{}".format(c))
              #----------------------------------------------------------------------#
              #ks test
              #----------------------------------------------------------------------#
              d, p_ks = stats.ks_2samp(p_list, c)

              if p_ks > small_value:
                  p_ks_final =  p_ks
              else:
                  p_ks_final = small_value

              #print("p_ks:{}" .format(p_ks_final))


              p_ks_finallist.append(p_ks_final)      

        fig = plt.figure()
        print("p_ks:{}".format(p_ks_finallist))
        _p_ks_finallist= np.array(p_ks_finallist)
        p_ks_finallist_log = -np.log10(_p_ks_finallist)
        print("p_ks_log:{}".format(p_ks_finallist_log))
        np.savetxt(result_dir+'/{}fp_ksplog_{}boot_slice{}.txt'.format(m,bootnum,slice),p_ks_finallist_log,fmt = '%s', delimiter=',')
        np.savetxt(result_dir+'/{}fp_ksp_{}boot_slice{}.txt'.format(m,bootnum,slice),p_ks_finallist,fmt = '%s', delimiter=',')

        #plt.scatter(x_axis2,p_ks_finallist_log)
        #plt.axhline(y=6.3, color='r')

        #fig.savefig(result_dir+'/{}tobs_slice{}_{}boot.png'.format(t_obs, slice, bootnum))
        #plt.show()