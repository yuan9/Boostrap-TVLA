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
F1 = open('ksplog_500boot.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
trace4 = np.array(file_split1, dtype = np.float32)


x_axis = []
for i in range(1,50):
      x = i * 20
      x_axis.append(x)

plt.plot(x_axis, trace1)

plt.plot(x_axis, trace2)

plt.plot(x_axis, trace3)

plt.plot(x_axis, trace4)
plt.xlabel("trace number")
plt.ylabel("ks_test_plog")
plt.axhline(y=6.3, color='r')
plt.legend(['100 boot','200 boot','300 boot','500 boot'], loc='upper left')
plt.show()