import sys
import pandas 
import numpy 
from matplotlib import pyplot as plt

row = int(sys.argv[2])

df = pandas.read_csv(sys.argv[1], header=None)
trace = df.to_numpy()

plt.plot(trace[row,:], lw = 0.5)
plt.show();
