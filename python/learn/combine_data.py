import pandas
import numpy
import csv
import sys
import math
import event

seq_file = sys.argv[1] 
vol_file = sys.argv[2]
signal_file = sys.argv[3]
output_fname = sys.argv[4]

df = pandas.read_csv(seq_file, header=None)
seq = df.iat[0,0]
print("seq", seq)

df = pandas.read_csv(vol_file, header=None)
vol = df.to_numpy()
vol = vol[0,:]
#print("vol", vol)

df = pandas.read_csv(signal_file, header=None)
exp_data = df.to_numpy()
exp_data = exp_data[0,:]
#print(exp_data)

norm_vol = event.normalize(vol)
norm_exp = event.normalize(exp_data)

out_file = open(output_fname, mode='w')

out_file.write('aa' +  ',' + 'volume' + ',' + 'normalized volume' + ',' 
        + 'left aa' + ',' + 'left vol' + ',' 
        + 'right_aa' + ',' + 'right vol' + ',' 
        + 'current' + ',' + 'normalized current' + ','
        + 'pos' + '\n')

for i in range(len(vol)):
    left_aa = ""
    left_vol = 0
    if (i > 0):
        left_aa = seq[i-1]
        left_vol = float(vol[i-1])
    right_aa = ""
    right_vol = 0
    if (i < len(vol) - 1):
        right_aa = seq[i+1]
        right_vol = float(vol[i+1])
    pos = 5
    if (i < pos):
        pos = i+1
    elif (len(vol) - i) < pos:
        pos = len(vol) - i
    out_file.write(seq[i] +  ',' + str(vol[i]) + ',' + str(norm_vol[i]) + ',' 
            + left_aa + ',' + str(left_vol) + ','
            + right_aa + ',' + str(right_vol) + ','
            + str(exp_data[i]) + ',' + str(norm_exp[i]) + ','
            + str(pos) + '\n')

out_file.close()
