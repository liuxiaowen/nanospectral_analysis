import numpy as np
import sys
import csv

ori_fname = sys.argv[1]
print("ori file name", ori_fname)
new_fname = sys.argv[2]
ori_data = np.genfromtxt(ori_fname, delimiter=',')

avg = np.mean(ori_data, axis= 0)

start_pos = np.argmin(avg[:5000])
end_pos = 5000 + np.argmin(avg[5000:])
size = end_pos - start_pos + 1
print("start pos", start_pos, " end pos ", end_pos, " size " , size)

new_file = open(new_fname, mode='w')
trace_writer = csv.writer(new_file, delimiter=',')

print(len(ori_data))
for i in range(len(ori_data)):
    row = ori_data[i,:]
    new_trace = row[start_pos:end_pos+1]
    trace_writer.writerow(new_trace);
