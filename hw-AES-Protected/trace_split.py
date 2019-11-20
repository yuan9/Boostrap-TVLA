#-------------------------------------------------------------------------#
# Yuan note: this script is used to spliting the traces with s=1 and s=2
#-------------------------------------------------------------------------#

import sys
import matplotlib.pyplot as plt
import numpy as np

linenum = 75790

fp="RawTraces.dwdb"
with open(fp) as f:
     for i,line in enumerate(f):
     		print("line-{}".format(i))
     		if i < linenum:
     			#print(line)
     			line_split=line.split(' ')
     			#print(line_split)

                # get the line label
     			for s in line.split(): 
     				if s.startswith('s='):
     					label = s

     			#print(label)	
     			

     			if label !='s=2':
     				#print("reach here")
     				f = open('RawTraces_new.dwdb', 'a+')
     				f.write(line)
     				f.close()	