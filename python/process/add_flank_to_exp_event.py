import csv
import sys
import math
import operator
import event
from event import *

exp_fname = sys.argv[1]
output_fname = sys.argv[2]
base = float(sys.argv[3])

add_len = 59

df = pandas.read_csv(exp_fname, header=None)
exp_events = df.to_numpy()

mean = numpy.mean(exp_events, axis=0)

size = len(mean)
print("length", size) 

first = float(mean[0])
last = float(mean[size-1])
start_trace = []
for i in range(add_len):
    h = first/add_len * i
    start_trace.append(h)

end_trace = []
for i in range(add_len): 
    h = last/add_len * (add_len - i - 1)
    end_trace.append(h)

trace_file = open(output_fname, mode='w')
trace_writer = csv.writer(trace_file, delimiter=',')

for i in range(len(exp_events)):
    ori_trace = exp_events[i,:]
    all_trace = numpy.concatenate(start_trace, ori_trace, end_trace)

    trace_len = len(all_trace)
    new_trace = []
    for j in range(size):
        pos = round(j / (size-1) * (trace_len-1))
        new_trace.append(trace[pos])

    trace_writer.writerow(new_trace)
