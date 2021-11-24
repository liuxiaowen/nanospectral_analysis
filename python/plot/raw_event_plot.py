import csv
import sys
import pandas 
import numpy 
import event
from matplotlib import pyplot as plt

start = int(sys.argv[2])
end = int(sys.argv[3])

df = pandas.read_csv(sys.argv[1], header=None)
trace = df.to_numpy()
trace = trace[start:end]

plt.plot(trace, lw = 0.5)
plt.show();
