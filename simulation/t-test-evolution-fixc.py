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
trace_num = 10000
bootnum = 400
fix_value = 5
result_dir = "fn_evolution"
#result_dir = "fp_evolution"
#result_dir = "fn_fvf_evolution"
if not os.path.exists(result_dir):
    os.mkdir(result_dir)
    #os.mkdir(result_dir+'/boot-p')


#----------------------------------------------------------#
# Read in the random set
#----------------------------------------------------------#
rand = []
fix = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/4.5327166168Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('rand_noise_10k.txt','r')
#F1 = open('rand_noise_trace10000.txt','r')
#F1 = open('Z:/simulation-trace/TP_SmallValue_set/1RandNoise_1000traces_0.01SNR_f5.txt','r')
#F1 = open('f4_noise_trace10000.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand = np.array(file_split1, dtype = np.float32)

#----------------------------------------------------------#
# Read in the rand comparison set
#----------------------------------------------------------#
rand2 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/4.5327166168Rand2Noise_1000traces_1SNR_f5.txt','r')
F1 = open('fix_noise_10k.txt','r')
#F1 = open('rand2_noise_trace10000.txt','r')
#F1 = open('Z:/simulation-trace/TP_SmallValue_set/1FixNoise_1000traces_0.01SNR_f5.txt','r')
#F1 = open('f5_noise_trace10000.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand2 = np.array(file_split1, dtype = np.float32)

#-------------------------------------------------------------#
# t-test
#--------------------------------------------------------------#
#t_list = []
#x_axis = []
#for i in range(1,100):

#    test_trace = i * 10      
#    t_obs2, p_obs2 = stats.ttest_ind(rand[0:test_trace-1],rand2[0:test_trace-1], equal_var = False)
#    t_list.append(abs(t_obs2))
#    x_axis.append(test_trace)

#print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
#plt.plot(x_axis,t_list)
#plt.axhline(y=4.5, color='r')
#plt.show()

#---------------------------------------------------------------------#
# Bootstrapping evlolution
#---------------------------------------------------------------------#


small_value = 1e-323 
x_axis2 = []
p_ks_finallist = []
#for i in range(1,51):
for i in range(1,100):
      #test_trace = i * 20
      test_trace = i * 10
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


      #c = np.random.uniform(0,1,test_trace)
      #generate uniform distribution
      #-------------------------------------------------------------------------------#
      #hypo = decimal.Decimal(count)/decimal.Decimal(bootnum)
      #step =  decimal.Decimal(1)/decimal.Decimal( test_trace)
      step =  float(1)/test_trace
      _c = []
      value = 0
      for i in range(0,test_trace):
          _c.append(value)
          value = value + step
      c = np.array(_c)
      #print(c)
      #target_list = c
      ##min = np.amin(target_list)
      ##max = np.amax(target_list)
      #min = 0
      #max =1
      #print("{}-{}".format(min,max))
      #bin_width = 0.01
      #print (bin_width)
      #bins_array = np.arange(min, max+bin_width, bin_width)
      ##plt.subplot(3,2,4)
      #plt.hist(target_list, bins=bins_array)
      #plt.title('p_log-random vs random') 
      #plt.ylabel('frequency') 
      #plt.show()

      #-------------------------------------------------------------------------------#
      np.savetxt(result_dir+'/uniform{}.txt'.format(bootnum),c,fmt = '%s', delimiter=',')

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
