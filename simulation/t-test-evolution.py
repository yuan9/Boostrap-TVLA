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

target_snr_db = 1
trace_num = 10000
bootnum = 100
fix_value = 5
result_dir = "fn_FvR_evolution"
#os.mkdir(result_dir)

#----------------------------------------------------------#
# Read in the random set
#----------------------------------------------------------#
rand = []
fix = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('rand_noise_10k.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand = np.array(file_split1, dtype = np.float32)

#----------------------------------------------------------#
# Read in the rand comparison set
#----------------------------------------------------------#
rand2 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand2Noise_1000traces_1SNR_f5.txt','r')
F1 = open('fix_noise_10k.txt','r')
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
for i in range(1,100):
    test_trace = i * 100      
    t_obs2, p_obs2 = stats.ttest_ind(rand[0:test_trace-1],rand2[0:test_trace-1], equal_var = False)
    t_list.append(abs(t_obs2))
    x_axis.append(test_trace)

#print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
plt.plot(x_axis,t_list)
plt.axhline(y=4.5, color='r')
plt.show()

#---------------------------------------------------------------------#
# Bootstrapping evlolution
#---------------------------------------------------------------------#

small_value = 1e-323 
x_axis2 = []
p_ks_finallist = []
for i in range(1,50):
      test_trace = i * 20
      t_list = []
      p_list = []
      t_obs2, p_obs2 = stats.ttest_ind(rand[0:test_trace-1],rand2[0:test_trace-1], equal_var = False)
      x_axis2.append(test_trace)
      print("{}-test-trace: {}".format(test_trace,abs(t_obs2)))
      for b in range(0, bootnum):
          random_list = np.random.randint(2*test_trace-1, size = 2*test_trace)
          boot_rand = []
          boot_rand2 = []
          for i in random_list:
              r = random.randint(0,1)
              #print(r)
              if r == 0:
                  boot_rand.append(rand[i%test_trace])
              if r == 1:
                  boot_rand2.append(rand2[i%test_trace])

          t_boot, p_boot = stats.ttest_ind(boot_rand,boot_rand2,  equal_var = False)
          t_list.append(t_boot)
          p_list.append(max(p_boot,small_value))


      c = np.random.uniform(0,1,test_trace)
      np.savetxt(result_dir+'/uniform{}.txt'.format(bootnum),c,fmt = '%s', delimiter=',')
      print(len(c))
      d, p_ks = stats.ks_2samp(p_list, c)

      if p_ks > small_value:
          p_ks_final =  p_ks
      else:
          p_ks_final = small_value

      print("p_ks:{}" .format(p_ks_final))


      p_ks_finallist.append(p_ks_final)

fig = plt.figure()
print(p_ks_finallist)
_p_ks_finallist= np.array(p_ks_finallist)
p_ks_finallist_log = -np.log10(_p_ks_finallist)

np.savetxt(result_dir+'/ksplog_{}boot.txt'.format(bootnum),p_ks_finallist_log,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/ksp_{}boot.txt'.format(bootnum),p_ks_finallist,fmt = '%s', delimiter=',')

plt.plot(x_axis2,p_ks_finallist_log)
plt.axhline(y=6.3, color='r')

fig.savefig(result_dir+'/evolution_{}boot.png'.format(bootnum))
plt.show()
