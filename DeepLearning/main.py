from extract_features import ExtractFeatures
import numpy as np
import pandas as pd


if __name__ == '__main__':
    index = [1, 2, 3, 4, 5, 6, 7]
    dtype = [('a', 'int32'), ('b', 'float32'), ('c', 'float32')]
    values = np.zeros(7, dtype=dtype)
    df = pd.DataFrame(values, index=index)

    print(df)

    extract = ExtractFeatures(df, 2)