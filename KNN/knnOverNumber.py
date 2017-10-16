import pandas as pd
import re
from knn import *
import math
import numpy as np

data = pd.read_csv('knn_result.csv')

length = {}


for i in range(0, len(data['len'])):
    movieNum = data['len'][i]
    if movieNum in length:
        length[movieNum] = tuple
        tuple[0] += 1
        tuple[1] += data['accuracy'][i]
        length[movieNum] = tuple
    else:
        tuple = [0, 0]
        length[movieNum] = tuple

accOverLen = []
number = []
for key in length:
    print length[key]
    number.append(length[key][0])
    accOverLen.append(float(length[key][1]) / float(length[key][0]))
    len1 = length[key][0]

result = pd.DataFrame()

result['accuracy'] = accOverLen
result['number'] = number
result['length'] = length.keys()

result.to_csv('knn_acc_over_len.csv')

