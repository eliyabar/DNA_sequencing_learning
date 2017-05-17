from dir_scanner import dirScanner
import math
import numpy as np
import pandas as pd


# maximum number (of hits) that we can get in a line.
max_hits = 1000
# number of cells
n = 100

max_normalize = 3

array = [0] * n

with open("full_file.cpn", 'r') as f:
    for i, line in enumerate(f):
        index = int(float(line.split()[2]) / (max_hits / (math.pow(10, math.log10(n)))))
        # print("line: " + str(i) + "  " + str(index))
        if index >= n:
            array[n - 1] += 1
        else:
            array[index] += 1

print("Array:\n", array)


def normalize(array):
    std = np.std(array)
    mean = np.mean(array)
    for i in range(len(array)):
        normalized_num = (array[i] - mean) / std
        if normalized_num > max_normalize:
            normalized_num = max_normalize
        elif normalized_num < -max_normalize:
            normalized_num = -max_normalize

        array[i] = normalized_num

    return array

def create_index_names():
    col_names = []
    col_index = 0
    while col_index < max_hits:
        col_str = str(int(col_index)) + '_'
        col_index += (max_hits / (math.pow(10, math.log10(n))))
        col_str += str(int(col_index))
        col_names.append(col_str)
    col_names[-1] += '+'
    return list(col_names)


normalized_array = normalize(array)
print("Normalized Array:\n", normalized_array)

print(create_index_names())
print(len(normalized_array), len(create_index_names()))




df = pd.DataFrame(normalized_array, index=create_index_names())
print(df)
