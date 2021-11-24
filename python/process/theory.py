import csv
import sys
import pandas
import numpy
import event

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

def get_theory_trace(vol, r, l):
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

def update_vol(vol):
    shift = 11.3
    l = len(vol)
    #print(vol)
    for i in range(5):
        vol[i] = vol[i] - (5 - i) * shift
        vol[l-1-i] = vol[l-1-i] - (5-i)*shift
    #print(vol)

def get_trace_from_vol(vol, trace_type, weight, size):
    if trace_type == "pos":
        update_vol(vol)
    empty_vol = numpy.zeros(1)
    #print(vol)
    ext_vol = []
    ext_vol.append(0)
    for i in range(len(vol)):
        ext_vol.append(vol[i])
    ext_vol.append(0)
    #print(ext_vol)
    raw_theory_trace = get_theory_trace(ext_vol, weight,size)
    return raw_theory_trace
