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

normalized_array = normalize(array)
print("Normalized Array:\n", normalized_array)


df = pd.DataFrame(normalized_array, columns=[1.100])
print(df)
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer)
writer.save()


