import csv
import pandas
import sys
import math
import numpy 
import event
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from signal import *


def get_encode(points, encode_name, weight):
    encode = []
    for j in range(len(points)):
        if (encode_name=="vol"):
            x = points[j].get_vol_encode()
        elif (encode_name=="vol_pos"):
            x = points[j].get_vol_pos_encode()
        elif (encode_name=="two_vol"):
            x = points[j].get_two_vol_encode()
        elif (encode_name=="two_vol_pos"):
            x = points[j].get_two_vol_pos_encode()
        elif (encode_name=="three_vol"):
            x = points[j].get_three_vol_encode()
        elif (encode_name=="three_vol_pos"):
            x = points[j].get_three_vol_pos_encode()
        elif (encode_name=="neighbor_vol_pos_hydro"):
            x = points[j].get_neighbor_vol_pos_hydro_encode()
        elif (encode_name=="neighbor_class"):
            x = points[j].get_neighbor_class_encode(weight)
        elif (encode_name=="neighbor_class_pos"):
            x = points[j].get_neighbor_class_pos_encode(weight)
        encode.append(x)
    return numpy.array(encode)

def train_eval(model, train_x, train_y, eval_x, eval_y):
    m = model.fit(train_x, train_y)
    train_pred_y = m.predict(train_x)
    train_error = comp_error(train_y, train_pred_y)
    train_pcc = event.pcc(train_y, train_pred_y)
    #print (m.coef_, m.intercept_)

    eval_pred_y = m.predict(eval_x)
    eval_error = comp_error(eval_y, eval_pred_y)
    eval_pcc = event.pcc(eval_y, eval_pred_y)
    return numpy.array([train_error, train_pcc, eval_error, eval_pcc])

def cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2):
    if model_name == 'linear':
        model = LinearRegression() 
    elif model_name == 'svm':
        #model = SVR(kernel='linear', C=0.0001, gamma='auto')
        model = SVR(kernel='poly')
    elif model_name == 'rf':
        model = RandomForestRegressor(n_estimators=20, max_depth=4, random_state=0)
    xs_1 = get_encode(points_1, encode_name, weight)
    xs_2 = get_encode(points_2, encode_name, weight)

    result_1 = train_eval(model, xs_1, ys_1, xs_2, ys_2)
    result_2 = train_eval(model, xs_2, ys_2, xs_1, ys_1)
    print(result_1)
    print(result_2)
    avg = (result_1 + result_2)/2
    #print("model", model_name, "weight", weight, "te",
    #        avg[0]/42, "ee", avg[2]/42, "encode", encode_name, "tc", avg[1], "ec", avg[3])
    te = avg[0]/42
    ee = avg[2]/42
    print(f'{te:.3f}', f'{ee:.3f}')


def comp_error(a, b):
    s = 0
    for i in range(len(a)):
        e = (a[i]-b[i]) * (a[i]-b[i])
        s = s + e
    return s

def comp_norm_error(a, b):
    avg_a = numpy.mean(a)
    avg_b = numpy.mean(b)
    norm_b = b /avg_b * avg_a
    # print("norm b", norm_b)
    s = 0
    for i in range(len(a)):
        e = (a[i]-norm_b[i]) * (a[i]-norm_b[i])
        s = s + e
    return s

def read_data(fname):
    df = pandas.read_csv(fname)
    data = df.to_numpy()
    points = []
    ys = []
    vs = []
    print("data length", len(data))
    for i in range(len(data)):
        d = Signal(data[i,:])
        points.append(d)
        y = d.get_norm_signal()
        ys.append(y)
        v = d.get_norm_volume()
        vs.append(v)
    #print(ys)
    #print(vs)
    ys = numpy.array(ys)
    return [points, ys, vs]


fname_1 = sys.argv[1]
print("file name 1", fname_1)
fname_2 = sys.argv[2]
print("file name 2", fname_2)

[points_1, ys_1, vs_1] = read_data(fname_1)
[points_2, ys_2, vs_2] = read_data(fname_2)
error_1 = comp_error(ys_1, vs_1)
error_2 = comp_error(ys_2, vs_2)
print("data error", error_1, error_2, (error_1 + error_2)/2)
pcc_1 = event.pcc(ys_1, vs_1)
pcc_2 = event.pcc(ys_2, vs_2)
print("data pcc", pcc_1, pcc_2, (pcc_1 + pcc_2)/2)

weight=0
model_name = "linear"
#model_name = "svm"
#model_name = "rf"
encode_name = "vol"
cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
encode_name = "vol_pos"
cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
encode_name = "two_vol"
cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
encode_name = "two_vol_pos"
cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
'''
encode_name = "three_vol"
cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
encode_name = "three_vol_pos"
cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
'''
for i in range(1):
    weight = 0.05 * i
    encode_name = "neighbor_class"
    cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 
    encode_name = "neighbor_class_pos"
    cross_validation(model_name, encode_name, weight, points_1, ys_1, points_2, ys_2) 

'''
de_norm_pred_y = de_normalize(eval_vol, norm_pred_y)
trace = compute_trace(de_norm_pred_y)

with open('ml_trace.csv', mode='w') as trace_file:
    trace_writer = csv.writer(trace_file, delimiter=',')
    trace_writer.writerow(trace)

from matplotlib import pyplot as plt
plt.plot(eval_y, label="Experimental")
plt.plot(eval_vol_y, label="Volume model")
plt.plot(pred_ey, label="Regression model")
#plt.plot(trace)
plt.legend()
plt.show()
'''
