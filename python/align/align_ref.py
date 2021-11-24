import pandas
import numpy
import csv
import sys
import event

theory_fname = sys.argv[1]
event_fname = sys.argv[2]
plot_fname = sys.argv[3]
print("theory file name", theory_fname)

df = pandas.read_csv(theory_fname, header=None)
theory_data = df.to_numpy()
#print(theory_data)
theory_spec = event.Event(0, theory_data[0,:])
#print(theory_data)
df = pandas.read_csv(event_fname, header=None)
exp_data = df.to_numpy()

avg = numpy.mean(exp_data, axis=0)
avg_spec = event.Event(0, avg)

[align_theory, dist] = event.alignment2(avg_spec.data, theory_spec.data)
#print("theory", theory_spec.data)
#print("average", avg_spec.data)
#print("aligned theory", align_theory)
norm_align_theory = event.normalize(align_theory)
print("dist", dist)
print("PCC between ref and avg", event.pcc(norm_align_theory, avg_spec.data));

from matplotlib import pyplot as plt
plt.rcParams.update({'font.size': 18})
plt.plot(align_theory, label="Theoretical")
plt.plot(avg_spec.data, label="Experimental")
plt.legend(loc='upper center', frameon=False, bbox_to_anchor=(0.5,1.2), ncol=2)
plt.xlabel("Time")
plt.ylabel("Normalized signal")
plt.tight_layout()
plt.savefig(plot_fname);
