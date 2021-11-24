import csv
import sys
import pandas
import numpy
import event
import theory

vol_fname = sys.argv[1]
output_fname = sys.argv[2]
weight = float(sys.argv[3])
size = int(sys.argv[4])
t = sys.argv[5]
df = pandas.read_csv(vol_fname, header=None)
vol = df.to_numpy()
vol = vol[0,:]

trace = theory.get_trace_from_vol(vol, t, weight, size)

trace_file = open(output_fname, mode='w')
trace_writer = csv.writer(trace_file, delimiter=',')
print("trace length", len(trace))
trace_writer.writerow(trace)
