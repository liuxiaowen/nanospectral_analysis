import sys
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

df = pd.read_csv(sys.argv[1], delimiter=" ")
data = df.to_numpy()

x = data[:,1]
y = data[:,2]

fs = 18
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)

for i in range(len(x)):
  if x[i] > y[i]:
    red_dot, = plt.plot(x[i], y[i], 'o', color ='red');
  else:
    blue_dot, = plt.plot(x[i], y[i], 'o', color = 'blue');

plt.legend([red_dot, blue_dot], ["N-terminus first", "C-terminus first"],
    prop={'size': fs}) 
plt.xlabel('Original nanospectral PCC', fontsize = fs)
plt.ylabel('Flipped nanospectral PCC', fontsize = fs)
plt.tight_layout()

#plt.show();
plt.savefig(sys.argv[2])

