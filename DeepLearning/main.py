from sklearn.linear_model import LogisticRegression
from extract_features import ExtractFeatures
from prepare_data import PrepareData
import numpy as np
import os

DATA_FILES_PATH = "../DataSavedInCSV"


def save_matrix_to_csv_file(file_name, data):
    np.savetxt(os.path.join(DATA_FILES_PATH,file_name), data, delimiter=",", fmt='%10.5f')


def load_matrix_from_csv_file(file_name):
    return np.genfromtxt(os.path.join(DATA_FILES_PATH,file_name), delimiter=',', dtype=int)


if __name__ == '__main__':

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=500)
    x_data, y_data = data.get_matrix()
    save_matrix_to_csv_file("x_data_window_50000.csv", x_data)
    save_matrix_to_csv_file("y_data_window_50000.csv", y_data)
    print(len(x_data))
    print(len(x_data[0]))

    # index = [1, 2, 3, 4, 5, 6, 7]
    # dtype = [('a', 'int32'), ('b', 'float32'), ('c', 'float32')]
    # values = np.zeros(7, dtype=dtype)
    # df = pd.DataFrame(values, index=index)
    #
    # print(df)
    #
    # extract = ExtractFeatures(df, 2)

    # clf = LogisticRegression()
    # clf.fit(x_matrix, y)
    # print('score Scikit learn train: ', clf.score(x_matrix, y))
    # print('score Scikit learn test: ', clf.score(X_test, Y_test))