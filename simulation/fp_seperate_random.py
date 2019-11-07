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
bootnum = 500
fix_value = 5
result_dir = "fp_seperate_random"
#os.mkdir(result_dir)

#----------------------------------------------------------#
# Read in the random set
#----------------------------------------------------------#
rand = []
fix = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.01631976779Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('Z:/simulation-trace/TP_SmallValue_set/99FixNoise_1000traces_0.01SNR_f5.txt','r')
#F1 = open('rand_noise.txt','r')
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
F1 = open('Z:/simulation-trace/TP_SmallValue_set/99RandNoise_1000traces_0.01SNR_f5.txt','r')
#F1 = open('fix_noise.txt','r')
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
p_ks_finallist = []
slice = 200
imax =  1000
#print(len(rand))
#print(imax)

#for i in range(0,1):
for i in range(0,imax):
      rand1_select = []
      rand2_select = []
      random_list = np.random.randint(slice, size = slice)
      for num in random_list:
        rand1_select.append(rand[num])
      random_list = np.random.randint(slice, size = slice)
      for num in random_list:
        rand2_select.append(rand[num])

      t_list = []
      p_list = []
      t_obs2, p_obs2 = stats.ttest_ind(rand1_select, rand2_select, equal_var = False)
      print("slice-{}: t{}".format(i, abs(t_obs2)))

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
                  boot_rand.append(rand1_select[k%slice])
              if r == 1:
                  boot_rand2.append(rand2_select[k%slice])
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
np.savetxt(result_dir+'/ksplog_tp{}boot.txt'.format(bootnum),p_ks_finallist_log,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/ksp_tp{}boot.txt'.format(bootnum),p_ks_finallist,fmt = '%s', delimiter=',')

#plt.scatter(x_axis2,p_ks_finallist_log)
#plt.axhline(y=6.3, color='r')

#fig.savefig(result_dir+'/{}tobs_slice{}_{}boot.png'.format(t_obs, slice, bootnum))
target_list = np.abs(p_ks_final)

min = 0
max = 1
print("{}-{}".format(min,max))
#bin_width = (max - min)/bin_num
bin_width = 0.01
bins_array = np.arange(min, max+bin_width, bin_width)
plt.hist(target_list, bins=bins_array)
plt.title('p_value-ks') 
plt.ylabel('frequency')

plt.show()