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

bv = DpawsTools.Binave(1, 1, kernel=DpawsTools.binave_hbin)

source_data = [
        ('1', np.array([1,2,3,4,5], dtype=np.uint8)),
        ('1', np.array([3,2,4,6,3], dtype=np.uint8)),
        ('0', np.array([4,1,2,3,2], dtype=np.uint8)),
        ('0', np.array([2,4,3,1,1], dtype=np.uint8)),
        ('0', np.array([5,4,3,2,4], dtype=np.uint8)),
        ('0', np.array([1,3,3,3,6], dtype=np.uint8)),
        ('1', np.array([2,6,3,1,4], dtype=np.uint8)),
        ]
source_data = list(zip(*source_data)) # Transform the data to be easy to split

traces = source_data[1]
print(traces)
classifiers = source_data[0]
print(classifiers)
bv.process(traces, classifiers)


gtpval = next(bv._gtests()) # gtest in p-value
chi2pval = next(bv._chi2tests()) # chi2 in p-value

print("gtpval:{}".format(gtpval))
print("chi2val:{}".format(chi2pval))
