import csv
import sys
import pandas
import numpy
import random
import event
import theory

vol_list=[ 168.8, 203.4, 141.7, 167.9, 237.6,
170.8, 91.5, 66.4, 105.6, 203.6, 
129.3, 122.1, 99.1, 167.3, 155.1, 
135.2, 161.1, 124.5, 171.3, 202.1]

def get_random_vol(l):
    v = []
    for i in range(l):
        n = random.randint(0,19)
        v.append(vol_list[n])
    return v

output_fname = sys.argv[1]
size = int(sys.argv[2])
sp_num = int(sys.argv[3])
weight = 0 
l = 42
t = 'pos'

trace_file = open(output_fname, mode='w')
trace_writer = csv.writer(trace_file, delimiter=',')

random.seed(1)
for i in range(sp_num):
    vol = get_random_vol(l)
    trace = theory.get_trace_from_vol(vol, t, weight, size)
    #print("trace length", len(raw_theory_trace))
    trace_writer.writerow(trace)
