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

a=sys.argv
result_dir = time.strftime("SimBoot_{}boot_{}traces_snr{}_f{}".format(a[1].strip(),a[4].strip(), a[2].strip(),a[3].strip()) + "-%Y-%m-%d_%H_%M")
os.mkdir(result_dir)

#----------------------------------------------------------#
# Read in the random set
#----------------------------------------------------------#
rand = []
fix = []
F1 = open('rand_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand = np.array(file_split1, dtype = np.float32)

#print (rand)
#----------------------------------------------------------#
# Read in the fix set
#----------------------------------------------------------#
F1 = open('fix_noise.txt','r')
#F1 = open('rand2_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
fix = np.array(file_split1, dtype = np.float32)

#print (fix)

t_obs, p_obs = stats.ttest_ind(fix,rand, equal_var = False)
print("obsv rand vs fix-t:{} p:{}".format(t_obs,p_obs))

#----------------------------------------------------------#
# Read in the rand comparison set
#----------------------------------------------------------#
rand2 = []
F1 = open('rand2_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
rand2 = np.array(file_split1, dtype = np.float32)
t_obs2, p_obs2 = stats.ttest_ind(rand,rand2, equal_var = False)
print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
#print (rand)

#--------------------------------------------------------------#
# boot on the random set
#--------------------------------------------------------------#
#bootnum = 10000
bootnum = int(a[1])
t_list = []
p_list = []
t_list2 = []
p_list2 = []
small_value = 1e-323 


for b in range(0, bootnum):
    random_list = np.random.randint(len(rand)-1, size = len(rand))
    boot_rand = []
    for i in random_list:
        #print(i)
        boot_rand.append(rand[i])

    t_boot, p_boot = stats.ttest_ind(fix, boot_rand, equal_var = False)
    #print(p_boot)
    t_list.append(t_boot)
    p_list.append(max(p_boot,small_value))
    #p_list.append(p_boot)

    t_boot2, p_boot2 = stats.ttest_ind(boot_rand,rand2,  equal_var = False)
    t_list2.append(t_boot2)
    p_list2.append(max(p_boot2,small_value))
    #p_list2.append(p_boot2)
    #print("boot-{}".format(b))

p_log_list = -np.log10(p_list)
p_log_list2 = -np.log10(p_list2)

_snr = a[2].strip()
np.savetxt(result_dir+'/plog_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),p_log_list,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/p_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),p_list,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/t_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),t_list,fmt = '%s', delimiter=',')

np.savetxt(result_dir+'/plog2_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),p_log_list2,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/p2_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),p_list2,fmt = '%s', delimiter=',')
np.savetxt(result_dir+'/t2_{}boot_{}traces_{}SNR.txt'.format(bootnum,len(rand),_snr),t_list2,fmt = '%s', delimiter=',')
    

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
plt.subplot(3,2,1)

plt.hist(target_list, bins=bins_array)
plt.title('p value-random vs fix') 
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
plt.subplot(3,2,3)
plt.hist(target_list, bins=bins_array)
plt.title('p_log value-random vs fix') 
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
plt.subplot(3,2,5)
plt.hist(target_list, bins=bins_array)
plt.title('t-random vs fix') 
plt.ylabel('frequency')
plt.axvline(x=abs(t_obs), color='lime')
avg = np.mean(target_list)
plt.axvline(x=avg, color='r')
#****************************************************************#
target_list = np.abs(p_list2)
#min = np.amin(target_list)
#max = np.amax(target_list)
min = 0
max =1
print("{}-{}".format(min,max))
#bin_width = (max - min)/bin_num
bin_width = 0.01
bins_array = np.arange(min, max+bin_width, bin_width)
plt.subplot(3,2,2)
plt.hist(target_list, bins=bins_array)
plt.title('p_value-random vs random') 
plt.ylabel('frequency') 

target_list = np.abs(p_log_list2)
#min = np.amin(target_list)
#max = np.amax(target_list)
min = 0
max =324
print("{}-{}".format(min,max))
bin_width = (max - min)/bin_num
bins_array = np.arange(min, max+bin_width, bin_width)
plt.subplot(3,2,4)
plt.hist(target_list, bins=bins_array)
plt.title('p_log-random vs random') 
plt.ylabel('frequency') 



target_list = np.abs(t_list2)
min = np.amin(target_list)
#max = np.amax(target_list)
min =0
max = np.amax(np.abs(t_list))
print("{}-{}".format(min,max))
bin_width = (max - min)/bin_num
bins_array = np.arange(min, max+bin_width, bin_width)
plt.subplot(3,2,6)
plt.hist(target_list, bins=bins_array)
plt.title('t-random vs random') 
plt.ylabel('frequency')
plt.axvline(x=abs(t_obs2), color='lime')
avg = np.mean(target_list)
plt.axvline(x=avg, color='r')


plt.subplots_adjust(top=0.88,bottom=0.11,left=0.125,right=0.9,hspace=0.5)
fig.suptitle('{}boot-{}traces-{}SNR-{}fix\n'.format(a[1].strip(),len(rand),_snr, a[3].strip()) + "obsv rand vs fix-t:{} p:{}\n".format(t_obs,p_obs) + "obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2) )
fig.set_size_inches(15,20)
fig.savefig(result_dir+'/distribution_{}boot_{}traces_{}SNR.png'.format(bootnum,len(rand), _snr))
plt.show()