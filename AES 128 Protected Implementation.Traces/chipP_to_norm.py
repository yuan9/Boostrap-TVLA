# To support both python 2 and python 3
from __future__ import absolute_import, division, print_function, with_statement

import numpy as np
import os
import re
import struct
import functools
import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

#import tensorflow as tf
#import keras

import aes_internals as aise
import dwdb_reader
import Dpaws 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm

meta = {}
p_value = Dpaws.TraceRead('yuan_chi_test.dwfm', metadata=meta)
#pt = meta['[]']
 
p_norm=[]
# transfer to standard normal distribution
for i in range(0, len(p_value)):
	value =  1-p_value[i]/2
	print (value)
	normal = norm.ppf(1-p_value[i]/2)
	p_norm.append(normal)
	
tr = np.array(p_norm)
Dpaws.TraceWrite(tr, tracefile='yuan_chi_test_norm.dwfm')

