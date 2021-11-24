import pandas
import numpy
import csv
import sys
import event

theory_fname = sys.argv[1]
opt_event_fname = sys.argv[2]
plot_fname = sys.argv[3]
current_fname = sys.argv[4]

df = pandas.read_csv(theory_fname, header=None)
theory_data = df.to_numpy()
theory_spec = event.Event(0, theory_data[0,:])
print("theo mean", theory_spec.mean, "theo var", theory_spec.variance)

df = pandas.read_csv(opt_event_fname, header=None)
opt_data = df.to_numpy()
opt_spec = event.Event(0, opt_data[0,:])

# order is important
[opt_align, dist] = event.alignment2(theory_spec.data, opt_spec.data)

#for i in range(50):
#    print(i, opt_align[i], theory_spec.data[i])

from matplotlib import pyplot as plt
plt.plot(theory_spec.data, label="Theoretical")
plt.plot(opt_align, label="Experimental")
plt.legend()
plt.savefig(plot_fname);

norm_opt_align = opt_spec.de_norm_intensity(opt_align)

seq_len = 42
data_len = len(norm_opt_align)
print("data len", data_len)
bin_size = (data_len - 1) / (seq_len + 1)
wing = 1
print("bin size", bin_size, "wing size", wing)

min_pos = numpy.argmin(norm_opt_align)
min_val = norm_opt_align[min_pos]
print("min", min_val)

current = []

for i in range(seq_len):
    pos = round(bin_size * (i+1))
    sample = norm_opt_align[pos-wing: pos+wing+1]
    mean = numpy.mean(sample)
    #print(i, pos, opt_align[pos])
    current.append(mean - min_val)

with open(current_fname, mode='w') as current_file:
    current_writer = csv.writer(current_file, delimiter=',')
    current_writer.writerow(current)

