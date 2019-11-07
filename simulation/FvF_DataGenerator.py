import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import sys
from scipy import stats

#definiations
target_snr_db = 2
trace_num = 10000
fix_value = 5
fix_value2 =4
offset = 1
#hamming weight counting function
def hw(x):
  return bin(x).count("1")

#------------------------------------------------#
# generate fix set 1
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
mean_noise = 0
noise_volts_fix = np.random.normal(mean_noise, np.sqrt(noise_avg_watts_fix), len(x_watts_fix))
#print("noise:{}".format(noise_volts_fix))
# Noise up the original signal
y_volts_fix = x_volts_fix + noise_volts_fix
#print("add noise fix:{}".format(y_volts_fix))
#np.savetxt('fix_noise.txt',y_volts_fix,fmt = '%f', delimiter=',')
np.savetxt('f5_noise_trace10000.txt',y_volts_fix,fmt = '%f', delimiter=',')


#------------------------------------------------#
# generate fix set 2
#------------------------------------------------#

x_volts_fix = np.empty(trace_num)
x_volts_fix.fill(fix_value2 + offset)
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
mean_noise = 0
noise_volts_fix = np.random.normal(mean_noise, np.sqrt(noise_avg_watts_fix), len(x_watts_fix))
#print("noise:{}".format(noise_volts_fix))
# Noise up the original signal
y_volts_fix2 = x_volts_fix + noise_volts_fix
#print("add noise fix:{}".format(y_volts_fix))
#np.savetxt('fix_noise.txt',y_volts_fix,fmt = '%f', delimiter=',')
np.savetxt('f4_noise_trace10000.txt',y_volts_fix2,fmt = '%f', delimiter=',')


#-------------------------------------------------#
# t-value calculation
#-------------------------------------------------#
t_list = []
x_axis = []
for i in range(1,101):

    test_trace = i * 100      
    t_obs2, p_obs2 = stats.ttest_ind(y_volts_fix[0:test_trace-1],y_volts_fix2[0:test_trace-1], equal_var = False)
    t_list.append(abs(t_obs2))
    x_axis.append(test_trace)

print("obsv rand vs rand-t:{} p:{}".format(t_obs2,p_obs2))
plt.plot(x_axis,t_list)
plt.axhline(y=4.5, color='r')
plt.show()