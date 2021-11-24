import numpy
import csv
import sys
import event

theory_fname = sys.argv[1]
event_fname = sys.argv[2]
print("theory file name", theory_fname)

theory_data = numpy.genfromtxt(theory_fname, delimiter=',')
#print(theory_data)
exp_data = numpy.genfromtxt(event_fname, delimiter=',')
event_num = len(exp_data) 
#event_num = 100

theory_spec = event.Event(0, theory_data)

exp_events = []
flip_events = []
for i in range(event_num):
    row = exp_data[i,:]
    #print("row", row)
    e = event.Event(i, row)
    exp_events.append(e)
    flipped_row = numpy.flip(row)
    #print(flipped_row)
    flipped_e = event.Event(i, flipped_row)
    flip_events.append(flipped_e)

event_num = len(exp_events)
count = 0
f = False

new_event_file = open(sys.argv[3], mode='w')
trace_writer = csv.writer(new_event_file, delimiter=',')

min_dist = []
for i in range(event_num):
    [align_exp, dist] = event.alignment2(theory_spec.data, exp_events[i].data)
    [flip_align_exp, flip_dist] = event.alignment2(theory_spec.data, flip_events[i].data)
    if (flip_dist < dist):
      min_dist.append(flip_dist)  
      count = count + 1
      f = True
      trace_writer.writerow(flip_events[i].raw_data)
    else:
      min_dist.append(dist)
      trace_writer.writerow(exp_events[i].raw_data)

    print(i, dist, flip_dist, (dist - flip_dist),f)

print("flipped", count)
print("avg dist", numpy.average(min_dist))
