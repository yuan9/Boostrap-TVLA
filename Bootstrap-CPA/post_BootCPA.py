#import tensorflow as tf
#import keras

#import aes_internals as aise
#import dwdb_reader

import numpy as np
import os
import re
import struct
import functools
import time
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import time
import util.dwdb_reader as io
import util.tests as tests


trace_num = 50000
step =  5000
boot_num = 10

result_dir = "Boot-CPA-Disinguisher-plot"
if not os.path.exists(result_dir):
  os.mkdir(result_dir)
#--------------------------------------------#
# Yuan: read_in traces
#--------------------------------------------#

#def plot_evolution(infile):
F1 = open('Boot-CPA-results/BootCPA_20boot_step5000.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")

file = []
for line in file_split1:
    line_list = []
    line = line.split(',')
    for data in line:
        #print ("data:{}".format(data))
        line_list.append(float(data))

    file.append(line_list)

file_np = np.array(file)
#the file array data structure is:
# keyguess-0 [d0, d1, d2, d3 ... dn] (n donates the steps in the evolution)
# keyguess-1 [d0, d1, d2, d3 ... dn]
# keyguess-2 [d0, d1, d2, d3 ... dn]

file_trans =  file_np.T
#the file array data structure is:
# t-0 [d0-key0, d1, d2, d3 ... d256] (n donates the steps in the evolution)
# t-1 [d0-key2, d1, d2, d3 ... d256]
# t-2 [d0-key3, d1, d2, d3 ... d256]


# time_data= [d0-key0, d2-key2, d3-key3 ... d10-key256]
plot_value = []
for time_data in file_trans:
    correct_value =  time_data[74]

    time_data.sort()
    if correct_value == time_data[-1]:
        plot_value.append(correct_value - time_data[-2])
    else:
        plot_value.append(correct_value - time_data[-1])

np.savetxt(result_dir+'/BootCPADistinguisher_{}boot_step{}.txt'.format(boot_num, step),plot_value,fmt = '%s', delimiter=',')
x_axis = []
# calculating the axis
for i in range(1, int(trace_num/step)+1):  # this is the iteration for the trane number evolution
	trace_range =  i * step
	x_axis.append(trace_range)


#------------------------------------------#
# plotting the traces
#------------------------------------------#
fig = plt.figure(figsize=(12,6.5))

font = {'family' : 'normal',  'size'   : 15}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'


plt.xlabel('Trace Number');
plt.ylabel('-log10(p) Difference');
plt.title('Boot-CPA-{}iterations'.format(boot_num))
plt.axhline(y=0, color='r',linewidth=1.5)


plt.plot(x_axis, plot_value, linewidth=1.5, linestyle='-', color = 'b')

fig.savefig(result_dir+'/BootcpaDis_{}boot_step{}_range{}.png'.format(boot_num, step, trace_num))

plt.show()