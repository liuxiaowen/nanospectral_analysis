import pandas
import numpy
import csv
import sys
import event

theory_fname = sys.argv[1]
event_fname = sys.argv[2]
avg_weight = int(sys.argv[3])
optimized_fname = sys.argv[4]
print("theory file name", theory_fname)

#df = pandas.read_csv(theory_fname, header=None)
#theory_data = df.to_numpy()
theory_data = numpy.genfromtxt(theory_fname, delimiter=',')
exp_data = numpy.genfromtxt(event_fname, delimiter=',')
event_num = len(exp_data) 

theory_spec = event.Event(0, theory_data)

exp_events = []
for i in range(event_num):
    row = exp_data[i,:]
    #print("row", row)
    e = event.Event(i, row)
    exp_events.append(e)

avg_data = numpy.mean(exp_data, axis=0)
avg_spec = event.Event(0, avg_data)

[new_ref, dist] = event.alignment2(avg_spec.data, theory_spec.data)
print("PCC between ref and avg", event.pcc(avg_spec.data, new_ref))

last = len(exp_events)
last = 50
consensus = avg_spec.data
for i in range(0, last):
    [align_event, dist] = event.alignment2(consensus, exp_events[i].data)
    consensus = event.weight_avg(consensus, i+avg_weight, align_event, 1)
    consensus = event.normalize(consensus)
    [new_ref, dist] = event.alignment2(consensus, theory_spec.data)
    print("PCC between ref and consensus",i, event.pcc(consensus, new_ref))

denorm_consensus = avg_spec.de_norm_intensity(consensus)
with open(optimized_fname, mode='w') as avg_file:
    avg_writer = csv.writer(avg_file, delimiter=',')
    avg_writer.writerow(denorm_consensus)
