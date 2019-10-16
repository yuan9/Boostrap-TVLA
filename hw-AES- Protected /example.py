import os

import numpy as np
from scipy.stats import ttest_ind, ks_2samp, norm

import util.dwdb_reader as io
import util.tests as tests

# dwdb location and name
db_basedir = r'.'
db_name = 'log.dwdb'
db_fullname = os.path.join(db_basedir, db_name)


#####     SIMPLE READ     #####
# Read one dwfm from 13850, 1000 samples
# io.read_trace(r'log\d0000\f0000.dwfm', 3850, 1000)

# From current directory
dsr = io.dwdb_reader(db_name)
# With another base directory
# dsr = io.dwdb_reader(db_name, r'data')

# Read one trace completely
one_trace = dsr.read_next()

# Read a batch of 20 traces, range [13850:13950)
tr_count = 20
data_batch, meta_batch = dsr.read_batch(tr_count, 13850, 13950)


#####     SIMPLE WRITE     #####
dsw = io.dwdb_writer(r'db_test\test2.dwdb', base_path=r'db_test')
dsw.write_batch(data_batch, meta_batch)
dsw.close()

#####     PROCESSING     #####

# Get classification
# meta example: -2354 jfilenem.dwfm  s=1 pt=alkshglkjsahgkhsaga ct=kjdsahgkjsahkjahsg
#classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('s=')]
classifiers = [m['classifiers'].strip('{}') for m in meta_batch]
traces = np.asarray(data_batch)
classifiers = np.asarray(classifiers)

# Split by generator to classify
fvr_cls = classifiers[np.where(classifiers != '2')]
fvr_traces = traces[np.where(classifiers != '2')]

fixed_traces  = fvr_traces[np.where(fvr_cls == '0')]
random_traces  = fvr_traces[np.where(fvr_cls == '1')]

# Get ttest
tt = tests.welch_ttest_fvr(fvr_traces, fvr_cls)
print('FvR tt results: {}'.format(tt))


# I. Calculate required distribution, according to the moments
# and generate the traces
trace_len, trace_count = 5, 100
moments0 = [ 1.6, 5^2]
moments1 = [-1.6, 4^2]
# with n = trace_count
# tt = (m0 - m1)/sqrt(s0^2/n+s1^2/n) = 5
# e.g. (1.6 - -1.6)/sqrt(25/10000 + 16/10000) = 5
# traces0 = tests.generate_dist(moments0, size=(trace_count, trace_len))
# traces1 = tests.generate_dist(moments1, size=(trace_count, trace_len))

# II. Another way to generate (faster, but 1st moment only)
trace_len, trace_count = 5, 100
traces0 = norm(loc= 1.6, scale=5).rvs(size=(trace_count, trace_len))
traces1 = norm(loc=-1.6, scale=4).rvs(size=(trace_count, trace_len))
traces0 = np.rint(traces0).astype(np.int8)
traces1 = np.rint(traces1).astype(np.int8)

trace_set = np.vstack((traces0, traces1))
cls_set   = ['0']*len(traces0) + ['1']*len(traces1)
tt = tests.welch_ttest_fvr(trace_set, cls_set)

print('Generated RvR with tt==5: {}'.format(tt))

print "done"
