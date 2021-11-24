import csv
import pandas
import numpy
import sys
import matplotlib.pyplot as plt

df = pandas.read_csv(sys.argv[1], header=None)
scores = df.to_numpy()
scores = scores[0,:]

plt.rcParams.update({'font.size': 18})
plt.hist(scores, bins = 50)
plt.xlabel("PCC")
plt.ylabel("# peptides")
plt.tight_layout()
plt.savefig(sys.argv[2])
