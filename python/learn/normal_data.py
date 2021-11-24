import pandas
import numpy
import csv
import sys
import math
import event

fname_1 = sys.argv[1] 
fname_2 = sys.argv[2]
norm_fname_2 = sys.argv[3]

df = pandas.read_csv(fname_1, header=None)
data_1 = df.to_numpy()
data_1 = data_1[0,:]
avg_1 = numpy.mean(data_1)

df = pandas.read_csv(fname_2, header=None)
data_2 = df.to_numpy()
data_2 = data_2[0,:]
avg_2 = numpy.mean(data_2)
print("avg 1", avg_1, "avg_2", avg_2)

for i in range(len(data_2)):
    data_2[i] = data_2[i]/avg_2 * avg_1

print("new avg", numpy.mean(data_2))

new_file = open(norm_fname_2, mode='w')
trace_writer = csv.writer(new_file, delimiter=',')
trace_writer.writerow(data_2)
