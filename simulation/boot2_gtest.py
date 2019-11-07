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

import Dpaws
import DpawsUtils
import DpawsTools
from DpawsTools import _iorw as iorw
from Dpaws.Common import RoundUp, RoundDown, bytes2hex as b2h, hex2bytes as h2b
from Dpaws.Crypto.AES import AES_TV
from Dpaws.Crypto.AES_FBC import AES_FBC_TV

a=sys.argv
result_dir = time.strftime("SimBoot2_{}boot_{}traces_snr{}_f{}".format(a[1].strip(),a[4].strip(), a[2].strip(),a[3].strip()) + "-%Y-%m-%d_%H_%M")
#result_dir = "test"
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
    random_list = np.random.randint(2*len(rand)-1, size = 2*len(rand))
    boot_rand = []
    boot_fix = []
    for i in random_list:
        r = random.randint(0,1)
        if r == 0:
            boot_fix.append(fix[i%len(rand)])
        if r == 1:
            boot_rand.append(rand[i%len(rand)])	

    t_boot, p_boot = stats.ttest_ind(boot_rand,boot_fix, equal_var = False)
    #print(p_boot)
    t_list.append(t_boot)
    p_list.append(max(p_boot,small_value))
    #p_list.append(p_boot)
	
    random_list = np.random.randint(2*len(rand)-1, size = 2*len(rand))
    boot_rand = []
    boot_rand2 = []
    for i in random_list:
        r = random.randint(0,1)
        if r == 0:
            boot_rand.append(rand[i%len(rand)])
        if r == 1:
            boot_rand2.append(rand2[i%len(rand)])

    t_boot2, p_boot2 = stats.ttest_ind(boot_rand,boot_rand2,  equal_var = False)
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

##----------------------------------------------------------------------------------------#
## Gtest for comparison p distribution with Uniform distribution
##----------------------------------------------------------------------------------------#boot
##generate a uniform distribution
##c = np.random.uniform(0,1,bootnum)

##_p_list=(10000*np.array(p_list)).astype('uint8')
#_p_list=(10000*np.array(p_list))
#print("p_list:{}".format(p_list))
#F1 = open('uniform.txt','r')
#file_string1 = F1.read()
#F1.close()
#file_split1 = file_string1.split("\n")[:-1]
##print(file_split1)
#_c = np.array(file_split1, dtype = np.float32)
#print("_c:{}".format(_c))
##c = (10000*_c).astype('uint8')
#c = 10000*_c
#print("c:{}".format(c))
#print("_p_list:{}".format(_p_list))
#p_c = np.concatenate((_p_list,c),axis=None)

#def split(arr, size):
#    arrs = []
#    while len(arr) > size:
#      pice = arr[:size]
#      arrs.append(pice)
#      arr = arr[size:]
#    arrs.append(arr)
#    return arrs

#trace = split(p_c,1)
#print("lentrace:{}".format(len(trace)))

#_zeros = np.zeros(len(c))
#_ones = np.ones(len(c))
#zeros = _zeros.astype(int)
#ones = _ones.astype(int)

#label = np.concatenate((ones,zeros),axis=None)
##label_str = label.astype(str)
#label_str = map(chr, np.array(label)+ord('0'))
#print("lenlabel:{}".format(len(label)))
## Binave with a histogram kernel
#binaveh = DpawsTools.Binave(1, 1, kernel=DpawsTools.binave_hbin) 
## I marked them with colors to explain the division better.
##print(trace)
##print(label_str)
#binaveh.process(trace, label_str)
#gtpval = next(binaveh._gtests()) # gtest in p-value
#chi2pval = next(binaveh._chi2tests()) # chi2 in p-value
#print("gtpval:{}".format(gtpval))
#print("chi2val:{}".format(chi2pval))
#-------------------------------------------------------------------------#
file_split1 = open('uniform.txt','r').read().split("\n")[:-1]
#print(file_split1)
_c = np.array(file_split1, dtype = np.float32)
#print("_c:{}".format(_c))
#c = (10000*_c).astype('uint8')
c = [_c[i:i+1] for i in range(len(_c))]
print("c:{}".format(c))

#_p_list=(10000*np.array(p_list)).astype('uint8')
_p_list=np.array(p_list)
p_list2 = [_p_list[i:i+1] for i in range(len(_p_list))]
#print("p_list:{}".format(p_list))

print("_p_list:{}".format(_p_list))

#def split(arr, size):
#    arrs = []
#    while len(arr) > size:
#      pice = arr[:size]
#      arrs.append(pice)
#      arr = arr[size:]
#    arrs.append(arr)
#    return arrs

#p_c = np.concatenate((_p_list,c),axis=none)
#trace = split(p_c,1)
#print("lentrace:{}".format(len(trace)))

## fix: zeros and ones generation
#zeros = ['0']*len(c)
#ones  = ['1']*len(c)
#label = np.concatenate((ones,zeros),axis=none)
#label_str = ones + zeros
#print("lenlabel:{}".format(len(label)))

# Binave with a histogram kernel
binaveh = DpawsTools.Binave(1, 1, kernel=DpawsTools.binave_hbin, bin_count=50) 
# I marked them with colors to explain the division better.
#print(trace)
#print(label_str)
binaveh.process(p_list2, ['0']*len(p_list2))
binaveh.process(c, ['1']*len(p_list2))

gtpval = next(binaveh._gtests()) # gtest in p-value
chi2pval = next(binaveh._chi2tests()) # chi2 in p-value
print("gtpval:{}".format(gtpval))
print("chi2val:{}".format(chi2pval))

#----------------------------------------------------------------------------------------#
# Gtest for comparison p distribution with Uniform distribution
#----------------------------------------------------------------------------------------#boot
#generate a uniform distribution
c = np.random.uniform(0,1,bootnum)

#F1 = open('uniform.txt','r')
#file_string1 = F1.read()
#F1.close()
#file_split1 = file_string1.split("\n")[:-1]
#print(len(p_list))


#c = np.array(file_split1, dtype = np.float32)
print(len(c))
d, p_ks = stats.ks_2samp(p_list, c)
t, p_t = stats.ttest_ind(p_list, c,  equal_var = False)

if p_ks > small_value:
    p_ks_final =  p_ks
else:
    p_ks_final = small_value

if p_t > small_value:
    p_t_final =  p_t
else:
    p_t_final = small_value

print("p_ks:{}" .format(p_ks_final))
print("p_t:{}" .format(p_t_final))