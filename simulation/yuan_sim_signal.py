import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import sys
from scipy import stats

#definiations
a=sys.argv
#target_snr_db = 20
#trace_num = 500
target_snr_db = float(a[2])
trace_num = int(a[1])
#fix_value = 5
fix_value = int(a[3])
offset = 1
#hamming weight counting function
def hw(x):
  return bin(x).count("1")
#----------------------------------------------#
# generate a random list
#----------------------------------------------#
random_list = np.random.randint(256, size = trace_num)
hw_randlist = []

for i in range(0,len(random_list)):
    hw_randlist.append(int(hw(random_list[i])))

#print("random list:{}".format(random_list))
#print("hw random list:{}".format(hw_randlist))

x_volts_orig = np.array(hw_randlist)
x_volts = x_volts_orig +  offset
np.savetxt('sig_orig.txt',x_volts,fmt = '%u', delimiter=',')
#plt.plot(x_volts)
#plt.show()

x_watts = x_volts ** 2
x_db = 10 * np.log10(x_watts)

#-----------------------------------------------#
# adding noise using target SNR
#-----------------------------------------------#
# Set a target SNR 

# Calculate signal power and convert to dB 
sig_avg_watts = np.mean(x_watts) 
sig_avg_db = 10 * np.log10(sig_avg_watts)
# Calculate noise according to [2] then convert to watts
noise_avg_db = sig_avg_db - target_snr_db 
noise_avg_watts = 10 ** (noise_avg_db / 10)
# Generate an sample of white noise
mean_noise = 0
noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))
#print("noise:{}".format(noise_volts))
# Noise up the original signal
y_volts = x_volts + noise_volts
#print("add noise:{}".format(y_volts))
#np.savetxt('rand_noise.txt',y_volts,fmt = '%f', delimiter=',')
np.savetxt('rand_noise_trace10000.txt',y_volts,fmt = '%f', delimiter=',')
#plt.plot(y_volts)
#plt.show()

#------------------------------------------------#
# generate fix set
#------------------------------------------------#

x_volts_fix = np.empty(trace_num)
x_volts_fix.fill(fix_value + offset)
x_volts_fix.astype(int)
#print("fix value:{}".format(x_volts_fix))

x_watts_fix = x_volts_fix ** 2
x_db_fix = 10 * np.log10(x_watts_fix)
sig_avg_watts_fix = np.mean(x_watts_fix) 
sig_avg_db_fix = 10 * np.log10(sig_avg_watts_fix)
# Calculate noise according to [2] then convert to watts
noise_avg_db_fix = sig_avg_db_fix - target_snr_db
noise_avg_watts_fix = 10 ** (noise_avg_db_fix / 10)
# Generate an sample of white noise
noise_volts_fix = np.random.normal(mean_noise, np.sqrt(noise_avg_watts_fix), len(x_watts_fix))
#print("noise:{}".format(noise_volts_fix))
# Noise up the original signal
y_volts_fix = x_volts_fix + noise_volts_fix
#print("add noise fix:{}".format(y_volts_fix))
#np.savetxt('fix_noise.txt',y_volts_fix,fmt = '%f', delimiter=',')
np.savetxt('fix_noise_trace10000.txt',y_volts_fix,fmt = '%f', delimiter=',')
#----------------------------------------------#
# generate a compare random list
#----------------------------------------------#
random_list = np.random.randint(256, size = trace_num)
hw_randlist = []

for i in range(0,len(random_list)):
    hw_randlist.append(int(hw(random_list[i])))


x_volts_orig = np.array(hw_randlist)
x_volts = x_volts_orig +  offset
np.savetxt('rand_orig.txt',x_volts,fmt = '%u', delimiter=',')

x_watts = x_volts ** 2
x_db = 10 * np.log10(x_watts)



# Calculate signal power and convert to dB 
sig_avg_watts = np.mean(x_watts) 
sig_avg_db = 10 * np.log10(sig_avg_watts)
# Calculate noise according to [2] then convert to watts
noise_avg_db = sig_avg_db - target_snr_db 
noise_avg_watts = 10 ** (noise_avg_db / 10)
# Generate an sample of white noise
mean_noise = 0
noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))

# Noise up the original signal
y_volts2 = x_volts + noise_volts

#np.savetxt('rand2_noise.txt',y_volts2,fmt = '%f', delimiter=',')
np.savetxt('rand2_noise_trace10000.txt',y_volts2,fmt = '%f', delimiter=',')
t_obs2, p_obs2 = stats.ttest_ind(y_volts,y_volts2, equal_var = False)
print("t_value:{}".format(t_obs2))
