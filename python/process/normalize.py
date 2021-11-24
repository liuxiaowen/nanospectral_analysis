import pandas
import numpy
import csv
import sys
import event

fname1 = sys.argv[1]
fname2 = sys.argv[2]
fname_out = sys.argv[3]

data1 = numpy.genfromtxt(fname1, delimiter=',')
data2 = numpy.genfromtxt(fname2, delimiter=',')

spec1 = event.Event(0, data1)
spec2 = event.Event(0, data2)

signal = spec2.data
signal = spec1.de_norm_intensity(signal)

new_spec = event.Event(0, signal)

print("spec 1 mean", spec1.mean, "spec 1 var", spec1.variance)
print("spec 2 mean", spec2.mean, "spec 2 var", spec2.variance)
print("new spec mean", new_spec.mean, "new spec var", new_spec.variance)

with open(fname_out, mode='w') as out_file:
    out_writer = csv.writer(out_file, delimiter=',')
    out_writer.writerow(signal)
