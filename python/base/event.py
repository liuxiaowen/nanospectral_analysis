import math

import numpy as np

class Event:
    def __init__(self, index, numbers):
        self.size = len(numbers)
        #print("size", self.size)
        self.index = index
        self.score = 0
        self.raw_data = np.zeros(self.size)
        for i in range(len(numbers)):
            self.raw_data[i] = float(numbers[i])
        #print(self.data)
        self.mean = self.comp_mean()
        self.variance = self.comp_variance()
        self.norm_intensity()
        #print('index ', self.index, 'size ', len(self.data), ' mean ', self.mean, ' variance ', self.variance)

    def comp_mean(self):
        s = 0
        for i in range(self.size):
            s = s + self.raw_data[i]
        return s/len(self.raw_data)

    def comp_variance(self):
        s = 0
        for i in range(self.size):
            s = s + (self.raw_data[i]-self.mean) * (self.raw_data[i]-self.mean)
        return s/len(self.raw_data)

    def norm_intensity(self):
        self.data = np.zeros(self.size)
        for i in range(self.size):
            self.data[i] = (self.raw_data[i] - self.mean)/math.sqrt(self.variance)

    def de_norm_intensity(self, a):
        b = []
        for i in range(self.size):
          b.append(a[i] * math.sqrt(self.variance) + self.mean)
        return b

    def set_score(self, s):
        self.score = s

    ''' 
    def norm_time(self):
        self.norm_data = []
        data_len = len(self.data)
        for i in range(self.norm_size):
            pos = round(i / (self.norm_size-1) * (data_len - 1))
            self.norm_data.append(self.data[pos])
        print('norm size ', len(self.norm_data))
        #print(self.norm_data)


    def smooth(self):
        self.smooth_data = []
        for i in range(24, self.norm_size-24):
            s = 0
            for j in range(i-12, i+12):
                s = s + self.norm_data[j]
            s = s/25
            self.smooth_data.append(s)
    '''

def average(events):
    average = [0] * len(events[0].data)
    for i in range(len(average)):
        for j in range(len(events)):
            average[i] = average[i]+events[j].data[i]
        average[i] = average[i]/len(events)
        #print('Average', i , 'len', len(events), 'intensity', average[i])
    return average

def dist(a,b):
    return (a-b)*(a-b)

def alignment2(x, y):
    len1 = len(x) + 2
    len2 = len(y) + 2
    t = np.zeros(shape = (len1, len2)) 
    b = np.zeros(shape = (len1, len2)) 
    # 0 is left, 1 is up, 2 is diag
    LEFT = 0
    UP = 1
    DIAG = 2
    t[0][0] = 0
    t[0][1] = 0
    t[1][0] = 0
    for i in range(2, len1):
        #t[i][0] = t[i-1][0]+ dist(x[i-2], 0)
        #t[i][1] = t[i-1][1]+ dist(x[i-2], 0)
        t[i][0] = 100000
        t[i][1] = 100000
        b[i][0] = UP
        b[i][1] = UP
    for j in range(2, len2):
        #t[0][j] = t[0][j-1] + dist(0, y[i-2])
        #t[1][j] = t[0][j-1] + dist(0, y[i-2])
        t[0][j] = 100000
        t[1][j] = 100000
        b[0][j] = LEFT
        b[1][j] = LEFT

    # fill up the table
    for i in range(2,len1):
        for j in range(2,len2):
            left = t[i-1][j-2] + dist(x[i-2], y[j-2])
            if (j >= 3):
                left = left + dist(x[i-2], y[j-3])
            up = t[i-2][j-1] + dist(x[i-2], y[j-2])
            if (i >= 3):
                up = up + dist(x[i-3], y[j-2])
            diag = t[i-2][j-2] + dist(x[i-2], y[j-2])
            if (i >= 3 and j >= 3):
                diag = diag + dist(x[i-3], y[j-3])
            if (diag <= left and diag <= up):
                t[i][j] = diag
                b[i][j] = DIAG
            elif left <= up:
                t[i][j] = left
                b[i][j] = LEFT
            else:
                t[i][j] = up
                b[i][j] = UP

    # backtracking
    #new_xa = np.arrange(len1)
    new_y = np.zeros(len2-2)
    i = len1-1
    j = len2-1
    total_dist = t[i][j]
    while (i >= 0 and j >= 0):
        if (i == 1 or i == 0):
            j = j -1
        elif (j == 1 or j == 0):
            new_y[i-2] = y[j-2]
            i = i - 1
        else:
            #print(i, j, "new_y", new_y[i-2], "y", y[j-2])
            if b[i][j] == DIAG:
                new_y[i-2] = y[j-2]
                if (j>=3):
                    new_y[i-3] = y[j-3]
                #print(i-1, new_y[i-1])
                i = i - 2
                j = j - 2
            elif b[i][j] == UP:
                new_y[i-2] = y[j-2]
                if (i>=3):
                    new_y[i-3] = y[j-2]
                #print(i-1, new_y[i-1])
                i = i - 2
                j = j - 1
            else:
                new_y[i-2] = y[j-2]
                i = i - 1
                j = j - 2
    new_y[0]=y[0]
    return [new_y, total_dist]

def sigma(a):
    s = 0
    for i in range(len(a)):
        s = s + a[i] * a[i]
    return math.sqrt(s)    

def cov(a, b):
    s = 0
    for i in range(len(a)):
        s = s + a[i] * b[i]
    return s

def pcc(a, b):
    sigma_a = sigma(a)
    sigma_b = sigma(b)
    c = cov(a,b)
    return c / (sigma_a * sigma_b)

def weight_avg(a, w_a, b, w_b):
    c = np.zeros(len(a))
    for i in range(len(a)):
        c[i] = (a[i] * w_a + b[i] * w_b) / (w_a + w_b)
    return c

def normalize(a):
    s = 0
    for i in range(len(a)):
        s = s + a[i]
    mean = s/len(a)

    s = 0
    for i in range(len(a)):
        s = s + (a[i]-mean) * (a[i]-mean)
    var = s/len(a)

    new_a = []

    for i in range(len(a)):
        new_a.append((a[i]- mean)/math.sqrt(var))
    return new_a

def convert_to_len_v3(trace, new_len):
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
        avg = np.average(sample)
        new_trace.append(avg)
    #add last poition
    new_trace.append(trace[size-1])
    #print("new trace length", len(new_trace))
    return new_trace
