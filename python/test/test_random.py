import numpy
import pandas
import csv
import sys
import event

consensus_fname = sys.argv[1]
random_fname = sys.argv[2]

df = pandas.read_csv(consensus_fname, header=None)
consensus_data = df.to_numpy()
#print(theory_data)
consensus = event.normalize(consensus_data[0,:])
#print(theory_data)
df = pandas.read_csv(random_fname, header=None)
random_data = df.to_numpy()

scores = []
for i in range(len(random_data)):
    random_trace = random_data[i,:]
    random_trace = event.normalize(random_trace)
    [align_random, dist] = event.alignment2(consensus, random_trace)
    score = event.pcc(consensus, align_random) 
    if i//100 * 100 ==i:
        print(i, "score", score)
    scores.append(score)

print("max score", numpy.amax(scores))

with open(sys.argv[3], mode='w') as score_file:
    score_writer = csv.writer(score_file, delimiter=',')
    score_writer.writerow(scores)

import matplotlib.pyplot as plt

plt.hist(scores, bins = 50)
plt.savefig(sys.argv[4])
