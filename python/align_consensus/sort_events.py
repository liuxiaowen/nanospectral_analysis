import pandas
import numpy
import csv
import sys
import event

event_fname = sys.argv[1]
sort_fname = sys.argv[2]

exp_data = numpy.genfromtxt(event_fname, delimiter=',')
event_num = len(exp_data) 
#event_num = 10

exp_events = []
for i in range(event_num):
    row = exp_data[i,:]
    #print("row", row)
    e = event.Event(i, row)
    exp_events.append(e)


avg = numpy.mean(exp_data, axis=0)
avg_spec = event.Event(0, avg)

scores = []
top_num = len(exp_events)
#top_num = 10
for i in range(top_num):
    [new_data,dist] = event.alignment2(avg_spec.data, exp_events[i].data)
    new_data = event.normalize(new_data)
    score = event.pcc(avg_spec.data, new_data) 
    print(i, "score", score, "dist", dist)
    scores.append([i,score])

scores.sort(key=lambda x: x[1], reverse=True)
print(scores)

sort_file = open(sort_fname, mode='w')
trace_writer = csv.writer(sort_file, delimiter=',')
for i in range(top_num):
    print(scores[i][0])
    trace_writer.writerow(exp_data[scores[i][0],:])
