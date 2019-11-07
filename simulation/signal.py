import numpy as np
from scipy.stats import distributions
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

t = np.linspace(1, 100, 1000)
x_volts = 10*np.sin(t/(2*np.pi)
plt.subplot(3,1,1) 
plt.plot(t, x_volts) 
plt.title('Signal') 
plt.ylabel('Voltage (V)') 
plt.xlabel('Time (s)') 
plt.show()