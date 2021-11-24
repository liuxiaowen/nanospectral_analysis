import sys
import pandas 
import numpy 
from matplotlib import pyplot as plt

df = pandas.read_csv(sys.argv[1], header=None)
ori_trace = df.to_numpy()

mean = numpy.mean(ori_trace, axis=0)

plt.plot(mean, lw = 1)
plt.savefig(sys.argv[2])
