import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import math
t = np.linspace(1, 100, 1000)
x_volts = 10*np.sin(t/(2*np.pi))
plt.subplot(3,1,1)
plt.plot(t, x_volts) 
plt.title('Signal') 
plt.ylabel('Voltage (V)') 
plt.xlabel('Time (s)') 
#plt.show()

x_watts = x_volts ** 2 
plt.subplot(3,1,2) 
plt.plot(t, x_watts) 
plt.title('Signal Power') 
plt.ylabel('Power (W)') 
plt.xlabel('Time (s)') 
#plt.show()

x_db = 10 * np.log10(x_watts) 
plt.subplot(3,1,3) 
plt.plot(t, x_db) 
plt.title('Signal Power in dB') 
plt.ylabel('Power (dB)') 
plt.xlabel('Time (s)') 
plt.show()

#-----------------------------------------------#
# adding noise using target SNR
#-----------------------------------------------#
# Set a target SNR 
target_snr_db = 0.01
#######################################################################
# Calculate signal power and convert to dB 
# sig_avg_watts = np.mean(x_watts) 
# sig_avg_db = 10 * np.log10(sig_avg_watts)
# # Calculate noise according to [2] then convert to watts
# noise_avg_db = sig_avg_db - target_snr_db 
# noise_avg_watts = 10 ** (noise_avg_db / 10)
# # Generate an sample of white noise
# mean_noise = 0
# noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts), len(x_watts))

##############################################################
mean_noise = 0
sigma_noise = math.sqrt(np.var(x_volts)/target_snr_db)
noise_volts = np.random.normal(mean_noise, sigma_noise, len(x_watts))
##################################################################
bin_num = 100
target_list = noise_volts
min = np.amin(target_list)
max = np.amax(target_list)
#min =0
#max = np.amax(np.abs(t_list))
print("{}-{}".format(min,max))
bin_width = (max - min)/bin_num
bins_array = np.arange(min, max+bin_width, bin_width)
plt.hist(target_list, bins=bins_array)
plt.title('noise') 
plt.ylabel('frequency')
plt.show()
###############################################################
# Noise up the original signal
y_volts = x_volts + noise_volts

# Plot signal with noise
plt.subplot(2,1,1) 
plt.plot(t, y_volts) 
plt.title('Signal with noise') 
plt.ylabel('Voltage (V)') 
plt.xlabel('Time (s)') 
#plt.show()

# Plot in dB 
y_watts = y_volts ** 2 
y_db = 10 * np.log10(y_watts) 
plt.subplot(2,1,2) 
plt.plot(t, 10* np.log10(y_volts**2)) 
plt.title('Signal with noise (dB)') 
plt.ylabel('Power (dB)') 
plt.xlabel('Time (s)') 
plt.show()