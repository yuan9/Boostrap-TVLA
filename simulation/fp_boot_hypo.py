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
fix = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/4.50026284862Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('rand_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand = np.array(file_split1, dtype = np.float32)

#----------------------------------------------------------#
# Read in the rand comparison set
#----------------------------------------------------------#
rand2 = []
#F1 = open('rand2_noise.txt','r')
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/4.50026284862Rand2Noise_1000traces_1SNR_f5.txt','r')
F1 = open('fix_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand2 = np.array(file_split1, dtype = np.float32)

#----------------------------------------------------------------#
diffmean_obs = abs(np.mean(rand) - np.mean(rand2))
t_obs2, p_obs2 = stats.ttest_ind(rand,rand2, equal_var = False)
print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
print("diffmean_obs:{}".format(diffmean_obs))
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
count2 = 0
for b in range(0, bootnum):
    random_list = np.random.randint(2*len(rand)-1, size = 2*len(rand))
    #print("random_list length:{}".format(len(random_list)))
    boot_rand = []
    boot_rand2 = []
    boot_merge = []
    for i in random_list:
        r = random.randint(0,1)
        #print(r)
        if r == 0:
            boot_merge.append(rand[i%len(rand)])
        if r == 1:
            boot_merge.append(rand2[i%len(rand)])

   # print("boot_merge length:{}".format(len(boot_merge))) 
    boot_rand = boot_merge[0:len(rand)] 
    #print(boot_rand[0:10])
    boot_rand2 = boot_merge[len(rand):2*len(rand)]
    #print(boot_rand2[0:10])
    diffmean_boot = abs(np.mean(boot_rand) - np.mean(boot_rand2))
    t_boot, p_boot = stats.ttest_ind(boot_rand,boot_rand2,  equal_var = False)
    #print(t_boot)
    #print (diffmean_boot)
    t_list.append(t_boot)
    p_list.append(max(p_boot,small_value))

    if abs(t_boot) >= abs(t_obs2):
        count = count + 1
    if diffmean_boot >= diffmean_obs:
        count2 = count2 + 1

print("count:{}".format(count))
print("count2:{}".format(count2))
p_log_list = -np.log10(p_list)
#hypo = float(count/bootnum)
hypo = decimal.Decimal(count)/decimal.Decimal(bootnum)
hypo2 = decimal.Decimal(count2)/decimal.Decimal(bootnum)
print ("hypo:{}".format(hypo))
print ("hypo2:{}".format(hypo2))
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
fig.suptitle('{}boot-{}traces-{}SNR-{}fix\n'.format(bootnum, trace_num, target_snr_db, fix_value) + "obsv rand vs fix-t:{} p:{}\n".format(t_obs2,p_obs2)+"boot_t_average:{}\n".format(avg) + "obsv rand vs fix-t:{} p:{}\n".format(t_obs2,p_obs2)+ "boot_hypo_statistics:{}\n".format(hypo)+"diffmean_boot_hypo_statistics:{}".format(hypo2))
fig.set_size_inches(15,20)
fig.savefig(result_dir+'/{}obsr_distribution_{}boot_{}traces_{}SNR.png'.format(t_obs2, bootnum,len(rand), _snr))
plt.show()