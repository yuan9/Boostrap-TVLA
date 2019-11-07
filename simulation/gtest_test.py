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

F1 = open('rand_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
_c = np.array(file_split1, dtype = np.float32)[0:10]
c = _c.astype(np.uint8)
#c = np.array(file_split1, dtype = np.uint8)[0:10]
F1 = open('fix_noise.txt','r')
file_string1 = F1.read()
F1.close()
file_split1 = file_string1.split("\n")[:-1]
#print(file_split1)
_p_list = np.array(file_split1, dtype = np.float32)[0:10]
#p_list = np.array(file_split1, dtype = np.uint8)[0:10]
p_list = _p_list.astype(np.uint8)
print(p_list)
p_c = np.concatenate((c,p_list),axis=None)

def split(arr, size):
    arrs = []
    while len(arr) > size:
      pice = arr[:size]
      arrs.append(pice)
      arr = arr[size:]
    arrs.append(arr)
    return arrs

trace = split(p_c,1)
print("lentrace:{}".format(trace))

_zeros = np.zeros(len(c))
_ones = np.ones(len(c))
zeros = _zeros.astype(int)
ones = _ones.astype(int)
label = np.concatenate((ones,zeros),axis=None)
print("lenlabel:{}".format(label))
#label_str = label.astype(str)
label_str = map(chr, np.array(label)+ord('0'))
print("lenlabel:{}".format(label_str))
# Binave with a histogram kernel
binaveh = DpawsTools.Binave(1, 1, kernel=DpawsTools.binave_hbin) 

#print(trace)
#print(label_str)

binaveh.process(trace, label_str)
gtpval = next(binaveh._gtests()) # gtest in p-value
chi2pval = next(binaveh._chi2tests()) # chi2 in p-value
t_obs2, p_obs2 = stats.ttest_ind(c,p_list, equal_var = False)
print("gtpval:{}".format(gtpval))
print("chi2val:{}".format(chi2pval))
print("ttest:{}".format(p_obs2))