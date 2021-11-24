import csv
import sys
import math
import operator
import event
from event import *

theory_fname = sys.argv[1]
print("theory file name", theory_fname)
output_fname = sys.argv[2]

# add len = 244 or 122
add_len = int(sys.argv[3])

with open(theory_fname) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    line = readCSV.__next__()

size = len(line)
print("length", size) 

first = float(line[0])
last = float(line[size-1])
trace = []
for i in range(add_len):
    h = first/add_len * i
    trace.append(h)

ori_trace = []
for i in range(size):
    ori_trace.append(float(line[i]))
    trace.append(float(line[i]))

for i in range(add_len): 
    h = last/add_len * (add_len - i - 1)
    trace.append(h)
trace_len = len(trace)
new_trace = []
for i in range(size):
    pos = round(i / (size-1) * (trace_len-1))
    new_trace.append(trace[pos])

with open(output_fname, mode='w') as trace_file:
    trace_writer = csv.writer(trace_file, delimiter=',')
    trace_writer.writerow(new_trace)
"""
from matplotlib import pyplot as plt
plt.plot(ori_trace)
plt.plot(new_trace)
plt.show()
"""
