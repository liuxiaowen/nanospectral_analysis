import csv
import sys
import pandas
import numpy
import event

def get_aaa_vol(vol, r):
    aaa_vol = []
    aaa_vol.append(0)
    l = len(vol)
    for i in range(l):
        if i > 0:
            left = vol[i-1] * r
        else:
            left = 0
        if i < l -1:
            right = vol[i+1] * r
        else:
            right = 0
        v = left + vol[i] + right
        aaa_vol.append(v)
    aaa_vol.append(0)
    return aaa_vol

def overlap(l1,r1,l2,r2):
    if (r1 <= l2 or r2 <= l1):
        return 0
    elif (l1 <= l2 and r1 >= l2 and r1 <= r2):
        return r1 - l2
    elif (l1 <= l2 and r1 >= r2):
        return r2 - l2
    elif (l1 >= l2 and r1 <= r2):
        return r1 - r1
    elif (l1 >= l2 and r1 >= r2):
        return r2 - l1

def get_theory_trace(vol, r):
    l = 1000
    trace = numpy.empty(l)
    vl = len(vol)
    pos = []
    w = (l-1)/(vl-1)
    #print("w", w)
    for i in range(vl):
        p = round(w * i)
        pos.append(p)
    #print(pos)
    total = 1 + 2* r
    wing = total/2
    for i in range(len(pos)-1):
        l = pos[i]
        r = pos[i+1]
        y1 = 0
        if (i > 0):
            y1 = vol[i-1]
        y2 = vol[i]
        y3 = vol[i+1]
        y4 = 0
        if (i < len(pos)-2):
            y4 = vol[i+2]
        for j in range(l,r+1):
            center = i + (j-l)/(r-l)
            left = center - wing
            right = center + wing
            r1 = overlap(left, right, i-1.5, i-0.5)
            r2 = overlap(left, right, i-0.5, i+0.5)
            r3 = overlap(left, right, i+0.5, i+1.5)
            r4 = overlap(left, right, i+1.5, i+2.5)
            #print(r1, r2, r3, r4)
            v = y1 * r1 + y2* r2 + y3 * r3 + y4 * r4;
            trace[j] = v
    return trace

def convert_to_200_v3(trace):
    new_len = 200
    size = len(trace)
    new_trace = []
    bin_size = size/(new_len-2)
    #print("bin size", bin_size) 
    #add the first poition
    new_trace.append(trace[0])
    for j in range(new_len-2):
        left = int(round(j*bin_size))  
        right =int(round((j+1)* bin_size))
        #print(left, right)
        if (right > size):
            right = size
        sample = trace[left:right]
        #print("sample size", len(sample))
        avg = numpy.average(sample)
        new_trace.append(avg)
    #add last poition
    new_trace.append(trace[size-1])
    #print("new trace length", len(new_trace))
    return new_trace

def convert_to_200(trace):
    new_len = 200
    size = len(trace)
    new_trace = []
    bin_size = size/(new_len-1)
    wing_size = bin_size/2
    #print("bin size", bin_size) 
    #add the first poition
    new_trace.append(trace[0])
    for j in range(new_len-2):
        left = int(round((j+1)*bin_size-wing_size))  
        right =int(round((j+1)* bin_size+wing_size))
        #print(left, right)
        if (right > size):
            right = size
        sample = trace[left:right]
        #print("sample size", len(sample))
        avg = numpy.average(sample)
        new_trace.append(avg)
    #add last poition
    new_trace.append(trace[size-1])
    #print("new trace length", len(new_trace))
    return new_trace

vol_fname = sys.argv[1]
output_fname = sys.argv[2]
df = pandas.read_csv(vol_fname, header=None)
vol = df.to_numpy()
vol = vol[0,:]

trace_file = open(output_fname, mode='w')
trace_writer = csv.writer(trace_file, delimiter=',')


empty_vol = numpy.zeros(1)
#print(vol)
ext_vol = []
ext_vol.append(0)
for i in range(len(vol)):
    ext_vol.append(vol[i])
ext_vol.append(0)
#print(ext_vol)

exp_fname = sys.argv[3]
df = pandas.read_csv(exp_fname, header=None)
exp_data = df.to_numpy()

avg = numpy.mean(exp_data, axis=0)
avg_spec = event.Event(0, avg)

test_num = 30
for i in range(test_num):
    r = i/100
    raw_theory_trace = get_theory_trace(ext_vol, r)
    theory_trace = convert_to_200_v3(raw_theory_trace)
    #print(theory_trace)
    trace_writer.writerow(raw_theory_trace)
    trace_spec = event.Event(0, theory_trace)
    [align_theory, dist] = event.alignment2(avg_spec.data, trace_spec.data)
    #print(len(align_theory))
    print("r", r,  "dist", dist, "pcc", event.pcc(align_theory, avg_spec.data))
