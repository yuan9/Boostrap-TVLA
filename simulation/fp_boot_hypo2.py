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
_snr = target_snr_db
trace_num = 1000
bootnum = 10000
#bootnum = 10
fix_value = 5
result_dir = "3fpcase_{}traces_snr{}_f{}".format(trace_num,target_snr_db,fix_value)
#os.mkdir(result_dir)

#----------------------------------------------------------#
# Read in the random set
#----------------------------------------------------------#
rand = []
_rand = []
fix = []
F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/4.5522633755Rand1Noise_1000traces_1SNR_f5.txt','r')
#F1 = open('rand_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
_rand = np.array(file_split1, dtype = np.float32)

#----------------------------------------------------------#
# Read in the rand comparison set
#----------------------------------------------------------#
rand2 = []
_rand2 = []
#F1 = open('rand2_noise.txt','r')
F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/4.5522633755Rand2Noise_1000traces_1SNR_f5.txt','r')
#F1 = open('fix_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
_rand2 = np.array(file_split1, dtype = np.float32)

#--------------------------------------------------------------#
merge = np.concatenate((_rand,_rand2), axis=None)
merge_mean = np.mean(merge)
rand = _rand - np.mean(_rand)+merge_mean
rand2 = _rand2 - np.mean(_rand2)+merge_mean


t_obs2, p_obs2 = stats.ttest_ind(_rand,_rand2, equal_var = False)
print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
#print (rand)

#--------------------------------------------------------------#
# boot on the random set
#--------------------------------------------------------------#

#bootnum = int(a[1])
t_list = []
p_list = []
t_list2 = []
p_list2 = []
small_value = 1e-323 

count = 0
for b in range(0, bootnum):
    random_list = np.random.randint(len(rand)-1, size = len(rand))
    boot_rand = []
    for i in random_list:
        #print(i)
        boot_rand.append(rand[i])
	
    random_list = np.random.randint(len(rand)-1, size = len(rand))
    boot_rand2 = []
    for i in random_list:
        #print(i)
        boot_rand2.append(rand2[i])

    t_boot, p_boot = stats.ttest_ind(boot_rand,boot_rand2,  equal_var = False)
    #print(t_boot)
    t_list.append(t_boot)
    p_list.append(max(p_boot,small_value))

    if abs(t_boot) >= abs(t_obs2):
        count = count + 1

print("count:{}".format(count))
p_log_list = -np.log10(p_list)
#hypo = float(count/bootnum)
hypo = decimal.Decimal(count)/decimal.Decimal(bootnum)
print ("hypo:{}".format(hypo))

np.savetxt(result_dir+'/plog_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),p_log_list,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/p_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),p_list,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/t_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),t_list,fmt = '%s', delimiter=',')

    

#----------------------------------------------------------#
# plot
#----------------------------------------------------------#
fig = plt.figure()
bin_num = 100
target_list = p_list
#min = np.amin(target_list)
#max = np.amax(target_list)
min = 0
max =1
print("{}-{}".format(min,max))
bin_width = float((max - min)/bin_num)
bin_width = 0.01
#print (bin_width)
bins_array = np.arange(min, max+bin_width, bin_width)
plt.subplot(3,1,1)

plt.hist(target_list, bins=bins_array)
plt.title('p value-random vs random') 
plt.ylabel('frequency') 
#plt.xlabel('value') 


target_list = np.abs(p_log_list)
#min = np.amin(target_list)
#max = np.amax(target_list)
min = 0
max =324
print("{}-{}".format(min,max))
bin_width = (max - min)/bin_num
bins_array = np.arange(min, max+bin_width, bin_width)
plt.subplot(3,1,2)
plt.hist(target_list, bins=bins_array)
plt.title('p_log value-random vs random') 
plt.ylabel('frequency') 
#plt.xlabel('value') 

target_list = np.abs(t_list)
#min = np.amin(target_list)
#max = np.amax(target_list)
min = 0
max = np.amax(np.abs(t_list))

print("{}-{}".format(min,max))
bin_width = (max - min)/bin_num
bins_array = np.arange(min, max+bin_width, bin_width)
plt.subplot(3,1,3)
plt.hist(target_list, bins=bins_array)
plt.axvline(x=abs(t_obs2), color='orange')
avg = np.mean(target_list)
plt.axvline(x=avg, color='r')
plt.title('t-random vs random') 
plt.ylabel('frequency')
#****************************************************************#

plt.subplots_adjust(top=0.88,bottom=0.11,left=0.125,right=0.9,hspace=0.5)
fig.suptitle('{}boot-{}traces-{}SNR-{}fix\n'.format(bootnum, trace_num, target_snr_db, fix_value) + "obsv rand vs fix-t:{} p:{}\n".format(t_obs2,p_obs2)+"boot_t_average:{}".format(avg) + "obsv rand vs fix-t:{} p:{}\n".format(t_obs2,p_obs2)+ "boot_hypo_statistics:{}".format(hypo))
fig.set_size_inches(15,20)
fig.savefig(result_dir+'/{}obsr_distribution_{}boot_{}traces_{}SNR.png'.format(t_obs2, bootnum,len(rand), _snr))
plt.show()