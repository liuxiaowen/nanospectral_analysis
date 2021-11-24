import sys
import pandas 
import numpy
import csv
import event

ori_fname = sys.argv[1]
print("ori file name", ori_fname)
df = pandas.read_csv(sys.argv[1], header=None)
ori_data = df.to_numpy()

l = int(sys.argv[2])

new_fname = sys.argv[3]
new_file = open(new_fname, mode='w')
trace_writer = csv.writer(new_file, delimiter=',')

print(len(ori_data))
for i in range(len(ori_data)):
    row = ori_data[i,:]
    new_trace = event.convert_to_len_v3(row, l)
    trace_writer.writerow(new_trace);
