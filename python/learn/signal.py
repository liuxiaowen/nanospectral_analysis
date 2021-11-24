import math

import numpy as np

hydroIndex = [("I", 4.5), ("V", 4.2), ("L", 3.8), ("F", 2.8), ("C", 2.5),
        ("M", 1.9), ("A", 1.8), ("G", -0.4), ("T", -0.7), ("S", -0.8),
        ("W", -0.9), ("Y", -1.3), ("P", -1.6), ("H", -3.2), ("E", -3.5),
        ("Q", -3.5), ("D", -3.5), ("N", -3.5), ("K", -3.9), ("R", -4.5)]

hydroDict = dict(hydroIndex)

class Signal:
    def __init__(self, items):
        self.amino_acid = items[0]
        self.volume = float(items[1])
        self.norm_volume = float(items[2])
        self.left_aa = items[3]
        self.left_volume = float(items[4])
        self.right_aa = items[5]
        self.right_volume = float(items[6])
        self.hydro_index = hydroDict[self.amino_acid]
        # print(self.amino_acid, self.hydro_index)
        self.current = float(items[7])
        self.norm_current = float(items[8])
        self.pos = int(items[9])

    def get_signal(self):
        return self.current

    def get_norm_signal(self):
        return self.norm_current

    def get_norm_volume(self):
        return self.norm_volume

    def get_volume(self):
        return self.volume

    def get_vol_encode(self):
        encode = []
        encode.append(self.volume)
        return encode

    def get_vol_pos_encode(self):
        encode = []
        encode.append(self.volume)
        encode.append(self.pos)
        return encode

    def get_two_vol_encode(self):
        encode = []
        encode.append(self.left_volume + self.right_volume)
        encode.append(self.volume)
        return encode

    def get_two_vol_pos_encode(self):
        encode = []
        encode.append(self.left_volume + self.right_volume)
        encode.append(self.volume)
        encode.append(self.pos)
        return encode

    def get_three_vol_encode(self):
        encode = []
        encode.append(self.left_volume)
        encode.append(self.volume)
        encode.append(self.right_volume)
        return encode

    def get_three_vol_pos_encode(self):
        encode = []
        encode.append(self.left_volume)
        encode.append(self.volume)
        encode.append(self.right_volume)
        encode.append(self.pos)
        return encode

    def get_neighbor_vol_pos_hydro_encode(self):
        encode = []
        encode.append(self.left_volume)
        encode.append(self.volume)
        encode.append(self.right_volume)
        encode.append(self.pos)
        encode.append(self.hydro_index)
        return encode

    def get_type(self, aa):
        aa_list = "GASCTDPNVEQHLIMKRFYW"
        pos = -1
        t = -1
        for i in range(20):
            if aa == aa_list[i]:
                pos = i
                break 
        if (pos >= 0 and pos <= 3):
            t = 0 
        elif (pos >= 4 and pos <= 8):
            t = 1 
        elif (pos >= 9 and pos <= 15):
            t = 2 
        elif (pos >= 16 and pos <= 19):
            t = 3 
        return t

    # this encoding method has the best performance so for
    def get_neighbor_class_encode(self, weight):
        encode = [0] * 4
        t = self.get_type(self.amino_acid)
        if (t >= 0):
            encode[t] = encode[t] + self.volume
        t = self.get_type(self.left_aa)
        if (t >= 0):
            encode[t] = encode[t] + self.left_volume * weight
        t = self.get_type(self.right_aa)
        if (t >= 0):
            encode[t] = encode[t] + self.right_volume * weight
        return encode

    def get_neighbor_class_pos_encode(self, weight):
        encode = [0] * 5
        t = self.get_type(self.amino_acid)
        if (t >= 0):
            encode[t] = encode[t] + self.volume
        t = self.get_type(self.left_aa)
        if (t >= 0):
            encode[t] = encode[t] + self.left_volume * weight
        t = self.get_type(self.right_aa)
        if (t >= 0):
            encode[t] = encode[t] + self.right_volume * weight
        encode[4] = self.pos
        return encode

'''
    def get_neighbor_class_2(self, weight):
        encode = [0] * 4
        t = self.get_type(self.amino_acid)
        if (t >= 0):
            encode[t] = encode[t] + self.volume
            encode[t] = encode[t] + self.left_volume * weight
            encode[t] = encode[t] + self.right_volume * weight
        return encode

    def get_neighbor_class_3(self, weight):
        encode = [0] * 12
        t = self.get_type(self.amino_acid)
        if (t >= 0):
            encode[t] = self.volume
        t = self.get_type(self.left_aa)
        if (t >= 0):
            encode[t+4] = self.left_volume
        t = self.get_type(self.right_aa)
        if (t >= 0):
            encode[t+8] = self.right_volume
        return encode

    def get_neighbor_class_4(self, weight):
        encode = [0] * 5
        t = self.get_type(self.amino_acid)
        if (t >= 0):
            encode[t] = encode[t] + self.volume
        t = self.get_type(self.left_aa)
        if (t >= 0):
            encode[t] = encode[t] + self.left_volume * weight
        t = self.get_type(self.right_aa)
        if (t >= 0):
            encode[t] = encode[t] + self.right_volume * weight
        if self.left_aa == "" or self.right_aa == "":
            encode[4] = 1
        return encode

    def get_one_hot(self):
        aa_list = "ACDEFGHIKLMNPQRSTVWY" #BJOUXZ are not amino acids
        encode = []
        for i in range(20):
            if self.amino_acid == aa_list[i]:
                encode.append(1)
            else:
                encode.append(0)
        return encode


    def get_class_encode(self):
        encode = [0] * 4
        t = self.get_type(self.amino_acid)
        if (t >= 0):
            encode[t] = self.volume
        return encode

    '''
