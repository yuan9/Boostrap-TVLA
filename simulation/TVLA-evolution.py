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
bootnum = 500
fix_value = 5
#result_dir = "fn_evolution"
#result_dir = "fp_evolution"
result_dir = "fn_fvf_evolution"
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


t_list = []
x_axis = []
for i in range(1,100):

    test_trace = i * 10      
    t_obs2, p_obs2 = stats.ttest_ind(rand[0:test_trace-1],rand2[0:test_trace-1], equal_var = False)
    t_list.append(abs(t_obs2))
    x_axis.append(test_trace)


font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'

plt.xlabel('Trace Number');
plt.ylabel('t-statistic');

#print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
plt.plot(x_axis,t_list,linewidth=2, linestyle='-', color = 'Navy')
plt.axhline(y=4.5, color='r')
plt.show()
