from __future__ import absolute_import, division, print_function, with_statement


import os
import re
import sys

import numpy as np
import matplotlib.pyplot as plt

# local imports
import util.tests as tests
import util.dwdb_reader as io
import util.func as f


ds_dir = 'FP_set' # source dataset

dsw = io.dwdb_writer(r'FP_db\log.dwdb', '', 'FP_db')

p = re.compile(r'(\d+)-(\d+)Rand(\d)Noise')

for dirName, subdirList, fileList in os.walk(ds_dir):
  print('Processing directory: {}'.format(dirName))
  for fname in fileList:
    m = p.search(fname)
    ctr, sn, s = m.group(1, 2, 3)
    fname2 = os.path.join(dirName, fname)
    # print('\t{} -> {}, {}, {}'.format(fname2, ctr, sn, s))
    tr = np.loadtxt(fname2)
    dsw.write_next(tr, {'ctr': ctr, 'sn' : sn, 's' : s})

