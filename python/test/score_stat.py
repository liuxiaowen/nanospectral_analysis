import csv
import pandas
import numpy
import sys

df = pandas.read_csv(sys.argv[1], header=None)
scores = df.to_numpy()
scores = scores[0,:]

print("average", numpy.mean(scores))
count = 0
for i in range(len(scores)):
    if scores[i] >= 0.94737:
        count = count+1
print("count", count)
