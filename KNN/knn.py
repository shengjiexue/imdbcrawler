import pandas as pd
import re
import math
import numpy as np


def getminDistance(data, tuple, start):

    # tuple is a dict with attributes same as data
    min1 = float('inf')

    for i in range(start, len(data['Country'])):
        sum1 = 0
        for key in data:
            if key == 'imdbID':
                continue
            sum1 += np.square(data[key][i] - tuple[key])
        if sum1 < min1 and sum1 != 0:
            min1 = sum1
            index1 = i
    return min1, index1
# read data
raw_data = pd.read_csv('output1.csv')
id = raw_data['imdbID']
del raw_data['imdbID']

data = raw_data

k = 1
instances = []
for i in range(0, k):
    tuple = {}
    for key in raw_data:
        tuple[key] = raw_data[key][i]
    instances.append(tuple)


distances = np.zeros((k, 2))
for tuple in range(0, k):

    (distance, index) = getminDistance(data, instances[tuple], k)
    distances[tuple, :] = (distance, index)

print distances



