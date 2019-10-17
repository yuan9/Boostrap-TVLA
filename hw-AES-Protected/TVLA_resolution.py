from __future__ import absolute_import, division, print_function, with_statement

import numpy as np
import os
import re
import struct
import functools
import time

import matplotlib
import matplotlib.pyplot as plt
#import pandas as pd

#import tensorflow as tf
#import keras

#import aes_internals as aise
import dwdb_reader
 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm
import seaborn as sns
import random
import util.dwdb_reader as io
import util.tests as tests


tracenum = 5

dsr = io.dwdb_reader('RawTraces.dwdb')
data_batch, meta_batch = dsr.read_batch(tracenum, 0, 300)
data_np = np.asarray(data_batch)


