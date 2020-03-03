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


tp_dir, fp_dir = 'TP_set', 'FP_set'
dsw_tp = io.dwdb_writer(r'TP_db.new\log.dwdb', '', 'TP_db.new')
dsw_fp = io.dwdb_writer(r'FP_db.new\log.dwdb', '', 'FP_db.new')

fpre = re.compile(r'(\d+)-(\d+)Rand(\d)Noise')
tpre = re.compile(r'(\d+)-(\d+)(tp|fix)_1000tr')

for dirName, subdirList, fileList in os.walk(tp_dir):
  print('Processing directory: {}'.format(dirName))
  for fname in fileList:
    m = tpre.search(fname)
    print("fname {} -> ".format(fname), end='')
    ctr, sn, s = m.group(1, 2, 3)
    print(ctr, sn, s)
    fname2 = os.path.join(dirName, fname)
    print('\t{} -> {}, {}, {}'.format(fname2, ctr, sn, s))
    tr = np.loadtxt(fname2)
    dsw_tp.write_next(tr, {'ctr': ctr, 'sn' : sn, 's' : int(s == 'tp')})

for dirName, subdirList, fileList in os.walk(fp_dir):
  print('Processing directory: {}'.format(dirName))
  for fname in fileList:
    m = fpre.search(fname)
    print("fname {} -> ".format(fname), end='')
    ctr, sn, s = m.group(1, 2, 3)
    print(ctr, sn, s)
    fname2 = os.path.join(dirName, fname)
    print('\t{} -> {}, {}, {}'.format(fname2, ctr, sn, s))
    tr = np.loadtxt(fname2)
    dsw_fp.write_next(tr, {'ctr': ctr, 'sn' : sn, 's' : int(s)})
