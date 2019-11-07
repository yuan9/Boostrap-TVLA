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


trace1 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('ksplog_100boot.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
trace1 = np.array(file_split1, dtype = np.float32)

trace2 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('ksplog_200boot.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
trace2 = np.array(file_split1, dtype = np.float32)


trace3 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('ksplog_300boot.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
trace3 = np.array(file_split1, dtype = np.float32)


trace4 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('ksplog_400boot.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
trace4 = np.array(file_split1, dtype = np.float32)

trace5 = []
#F1 = open('rr_1000traces_snr1_f5-2019-07-30_15_09/5.28109118925Rand1Noise_1000traces_1SNR_f5.txt','r')
F1 = open('ksplog_500boot.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
trace5 = np.array(file_split1, dtype = np.float32)



x_axis = []
for i in range(1,100):
      x = i * 10
      x_axis.append(x)

font = {'family' : 'normal',  'size'   : 30}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'

plt.xlabel('Trace Number');
plt.ylabel('-log10(p) of KS-test');

#plt.plot(x_axis, trace1,label='Boot 100 times',linewidth=2.5, linestyle='-', color = 'gray')
plt.plot(x_axis, trace2,label='Boot 200 times',linewidth=2.5, linestyle='-',  color = 'black')
plt.plot(x_axis, trace3,label='Boot 300 times',linewidth=2.5, linestyle='-',  color = 'g')
plt.plot(x_axis, trace4,label='Boot 400 times',linewidth=2.5, linestyle='-',  color = 'slateblue')
plt.plot(x_axis, trace5,label='Boot 500 times',linewidth=2.5, linestyle='-',  color = 'orange')

#plt.plot(x_axis, trace2,label='Boot 200 times',linewidth=2.5, linestyle='-', marker='o', markersize=10, color = 'black')
#plt.plot(x_axis, trace3,label='Boot 300 times',linewidth=2.5, linestyle='-', marker='x', markersize=10, color = 'g')
#plt.plot(x_axis, trace4,label='Boot 400 times',linewidth=2.5, linestyle='-', marker='v', markersize=10, color = 'slateblue')
#plt.plot(x_axis, trace5,label='Boot 500 times',linewidth=2.5, linestyle='-', marker='.', markersize=10, color = 'orange')

#plt.plot(x_axis, trace2,label='Boot 200 times',linewidth=2.5, linestyle='-', marker='o', markersize=10, color = 'black')
#plt.plot(x_axis, trace3,label='Boot 300 times',linewidth=2.5, linestyle='-', marker='x', markersize=10, color = 'black')
#plt.plot(x_axis, trace4,label='Boot 400 times',linewidth=2.5, linestyle='-', marker='v', markersize=10, color = 'black')
#plt.plot(x_axis, trace5,label='Boot 500 times',linewidth=2.5, linestyle='-', marker='.', markersize=10, color = 'black')

#plt.xlabel("trace number")
#plt.ylabel("ks_test_plog")
plt.axhline(y=6.3, color='r',linewidth=2.5)
plt.legend(loc='upper left')
#plt.legend(['100 boot','200 boot','300 boot','400 boot','500 boot'], loc='upper left')
plt.show()
