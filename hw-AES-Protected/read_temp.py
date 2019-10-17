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
import time

start_time = time.time()

strt_pt = 35
stop_pt = 215

sample_num = stop_pt - strt_pt + 1

overthr_count  = []
max = []
X=[]
#Yuan: resolution of the power value
resolution = 256

test_sample =  stop_pt - strt_pt + 1
test_trace = 500
op_len = 500
print ("readin files")

counter = 0
with open('slog_test.dwdb') as file:
    for cnt, line in enumerate(file):
        print("line{}:{}".format(cnt,line))
        line2 = dwdb_reader.parse_metadata_line(line)
        operation = dwdb_reader.read_trace(line2['filename'], -int(line2['offset']), op_len)
        #trace = dwdb_reader.read_trace(line2['filename'])[strt_pt:stop_pt]
        tr = np.array(operation)
        Dpaws.TraceWrite(tr, tracefile='bulktrace_readtest/trace{}.dwfm'.format(cnt))
print ("finish reading files")
    
# meta = []

# for line in content:
    # #print ("reach here")
    # meta.append(dwdb_reader.parse_metadata_line(line))
    # #meta.append(Dpaws.parse_metadata_line(line))
# #print(meta[0])
# #print ("total length:")
#print (len(meta))


# for i in range(0,500):
    # #while i < len(meta):
    # #trace = dwdb_reader.read_trace(meta[i]['filename'])[strt_pt:stop_pt]
    # trace = dwdb_reader.read_trace(meta[i]['filename'])[strt_pt:stop_pt]
    # tr = np.array(trace)
    # max = abs(np.amax(tr))
    # print("max:"+str(max))
    # min = abs(np.amin(tr))
    # print("min:"+str(min))
    # if max >= 256 or min <0:
        # print("datatype error")
    # #Dpaws.TraceWrite(tr, tracefile='chi_result/test1.dwfm')
    # #print("trace_length:" + str(len(trace)))
    # X.append(trace)
    # #X.append(Dpaws.read_trace(meta[i]['filename']))