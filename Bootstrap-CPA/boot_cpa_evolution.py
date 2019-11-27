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

#import aes_internals as aise
#import dwdb_reader
 
import numpy as np
import array
from scipy import stats
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import norm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random
import time
import util.dwdb_reader as io
import util.tests as tests

#Yuan: set evolution value
trace_num = 50000
step =  5000
boot_num = 10
# trace_num = 5000
# step =  1000
# boot_num = 2

#Yuan: set analysis target sample
start_sample = 10
end_sample =  11

small_value =  1e-323

result_dir = "Boot-CPA-results"
if not os.path.exists(result_dir):
  os.mkdir(result_dir)

print("reading traces")
dsr = io.dwdb_reader('/Users/yaoyuan/Desktop/Boostrap-TVLA/Bootstrap-CPA/trace.dwdb', '/Users/yaoyuan/Desktop/Boostrap-TVLA/Bootstrap-CPA/')
data_batch, meta_batch = dsr.read_batch(trace_num, start_sample, end_sample)
data_np = np.asarray(data_batch)

#processing of classifiers
classifiers = [s.split('=')[1] for m in meta_batch for s in m['other'].split() if s.startswith('hw=')]
classifiers = np.asarray(classifiers)
_classrifiers = []
for hw in classifiers:
	_classrifiers.append(hw.split(','))

classifiers2 =  (np.asarray(_classrifiers)).astype(int)

#print(data_np)
#print(classifiers2)

pc_evolution = []
p_evolution = []
x_axis = []
p = []
plog_ks_evolution=[]
# plog_ks_evolution 2D array
# trace_num1:  [p-keyguess1, p-keyguess2, p-keyguess3....]
# trace_num2:  [p-keyguess1, p-keyguess2, p-keyguess3....]
# ...
# trace_numn:  [p-keyguess1, p-keyguess2, p-keyguess3....]
for i in range(1, int(trace_num/step)+1):  # this is the iteration for the trane number evolution
	trace_range =  i * step 
	x_axis.append(trace_range)
	print("attacking on {} traces".format(trace_range))
	
	data_bootorig = data_np[0:trace_range].T[0]
	classifiers_bootorig = classifiers2[0:trace_range]
	#print(data_bootorig)
	#print(classifiers_bootorig)
    
    #------------------------------------------------#
    # Yuan: Bootstrap procedure
    #------------------------------------------------#

	p_full = []
	for b in range(0, boot_num):  # this is the iteration for the bootstrap
		data_boot = []
		classifiers_boot = []
		p_per_boot =[]
		pc_per_boot =[]
		#print("boot number: {}".format(b))
		random_list = np.random.randint(len(data_bootorig)-1, size = len(data_bootorig))
		random_list.sort()
	
		for number in random_list:
			data_boot.append(data_bootorig[number])
			classifiers_boot.append(classifiers_bootorig[number])

		classifiers_boot_trans = (np.asarray(classifiers_boot)).T
		#print(classifiers_boot)
		#print (data_boot)

		for keyguess in classifiers_boot_trans:
			pc, p = stats.pearsonr(data_boot, keyguess)
			p_per_boot.append(p)  # [p1,p2,p3......p256] for each keyguess
			pc_per_boot.append(pc) # [pc1, pc2, pc3 ... pc256] for each keyguess
		#print("p_per_boot: {}".format(p_per_boot))
		# 2D array: p_full
		# boot1[p1, p2....p256]
		# boot2[p1, p2....p256]
		# ...
		# bootn[p1, p2....p256]
		p_full.append(p_per_boot)
		#print("p_full:{}".format(p_full))
    #------------------------------------------------#
    # Yuan: ks-test procedure
    #------------------------------------------------#   

	# 2D array: p_full_trans
	# key1[p1, p1....p1]
	# key2[p2, p2....p2]
	# ...
	# key256[p256, p256....p256]

	p_full_trans = np.asarray(p_full).T
	#print("p_full:{}".format(p_full))
	#print("p_full_trans:{}".format(p_full_trans))
	# p_ks = [p-keyguess1, p-keyguess2, p-keyguess3....]
	p_ks = []
	for keyp in p_full_trans:
		d, p_ks_value = stats.kstest(keyp, 'uniform')
		#print("p_ks:{}".format(p_ks_value))
		if p_ks_value > small_value:
			p_ks_final =  p_ks_value
		else:
			p_ks_final = small_value
		p_ks.append(p_ks_final)

	plog_ks = -np.log10(np.asarray(p_ks))

	plog_ks_evolution.append(plog_ks)

plog_ks_evolution_trans = (np.asarray(plog_ks_evolution)).T
np.savetxt(result_dir+'/BootCPA_{}boot_step{}.txt'.format(boot_num, step),plog_ks_evolution_trans,fmt = '%s', delimiter=',')
#----------------------------------------------------------#
# plotting the result
#----------------------------------------------------------#

fig = plt.figure(figsize=(12,6.5))

font = {'family' : 'normal',  'size'   : 15}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'


plt.xlabel('Trace Number');
plt.ylabel('-log10(p)');
plt.title('Boot-CPA-{}iterations'.format(boot_num))

for i in range(0, len(plog_ks_evolution_trans)):
	if i == 74:
		plt.plot(x_axis, plog_ks_evolution_trans[i], linewidth=1.5, linestyle='-', color = 'r', zorder=255)	
	else:
		plt.plot(x_axis, plog_ks_evolution_trans[i], linewidth=1.5, linestyle='-', color = 'grey', zorder = i)	

fig.savefig(result_dir+'/BootCPA_{}boot_step{}_range{}.png'.format(boot_num, step, trace_num))	

plt.show()