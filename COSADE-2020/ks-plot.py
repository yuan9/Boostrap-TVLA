import numpy as np
import matplotlib.pyplot as plt

# normal data
data = [1, 12,34,56,34,101, 140,135,137,123,145,148,134,118, 121, 103, 142, 111, 119, 122, 128, 112, 117,157,178,190,167,200]
raw_data = np.array(data)
# create a sorted series of unique data
cdfx = np.sort(np.unique(data))
# x-data for the ECDF: evenly spaced sequence of the uniques
x_values = np.linspace(start=min(cdfx),stop=max(cdfx),num=len(cdfx))
    
# size of the x_values
size_data = raw_data.size
# y-data for the ECDF:
y_values = []
for i in x_values:
# all the values in raw data less than the ith value in x_values
	temp = raw_data[raw_data <= i]
        # fraction of that value with respect to the size of the x_values
	value = float(temp.size) / float(size_data)
	# pushing the value in the y_values
	y_values.append(value)
# return both x and y values    

print (x_values)
print (y_values)

# random data
raw_data2 = np.random.randint(200, size=size_data)
# create a sorted series of unique data
cdfx2 = np.sort(np.unique(raw_data2))
# x-data for the ECDF: evenly spaced sequence of the uniques
x_values2 = np.linspace(start=min(cdfx2),stop=max(cdfx2),num=len(cdfx2))
    
# size of the x_values
size_data2 = raw_data2.size
# y-data for the ECDF:
y_values2 = []
for i in x_values2:
# all the values in raw data less than the ith value in x_values
	temp2 = raw_data2[raw_data2 <= i]
        # fraction of that value with respect to the size of the x_values
	value2 = float(temp2.size) / float(size_data2)
	# pushing the value in the y_values
	y_values2.append(value2)
# return both x and y values    

print (x_values2)
print (y_values2)

font = {'family' : 'normal',  'size'   : 20}
plt.rc('font', **font)
plt.rcParams['figure.facecolor'] = 'white'

plt.xlabel('X');
plt.ylabel('Empirical Distribution Function');


plt.step(x_values,y_values, where='post', label='Data-set A',linewidth=2, linestyle='-', color = 'k')
plt.step(x_values2,y_values2, where='post', label='Data-set B',linewidth=2,linestyle='--', color = 'grey')
#plt.plot(x_values, y_values)
plt.legend(loc = 'upper left')
plt.show()
