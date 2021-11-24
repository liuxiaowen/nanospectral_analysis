import csv
import sys
import pandas 
import numpy 
import event

basename = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])

total_s = 0
total_n = 0
for j in range(start, end+1):
    fname = basename + str(j) + ".csv"
    df = pandas.read_csv(fname, header=None)
    trace = df.to_numpy()
    trace = trace[:,0]
    mean = numpy.mean(trace)
    # print("avg", mean)
    s = 0
    n = 0
    for i in range(len(trace)):
        if abs(trace[i]-mean) < 40:
            s = s + trace[i]
            n = n + 1
    total_s = total_s + s
    total_n = total_n + n
    print(fname, s/n)
print("total", total_s/total_n)
