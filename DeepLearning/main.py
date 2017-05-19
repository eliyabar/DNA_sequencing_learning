from sklearn.linear_model import LogisticRegression
from extract_features import ExtractFeatures
from prepare_data import PrepareData
import numpy as np
import os
import pandas as pd

DATA_FILES_PATH = "../DataSavedInCSV"


def save_all_data_to_CSVs():

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=500)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_50000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")
    np.savetxt(os.path.join(DATA_FILES_PATH, "y_data.csv"), y_data, delimiter=",", fmt='%10.5f', header="y", comments="")

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=100)
    x_data, y_data = data.get_matrix()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_10000.csv"), x_data, delimiter=",", fmt='%10.5f')

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=10)
    x_data, y_data = data.get_matrix()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_1000.csv"), x_data, delimiter=",", fmt='%10.5f')

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=1)
    x_data, y_data = data.get_matrix()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_100.csv"), x_data, delimiter=",", fmt='%10.5f')


def load_data_from_csv_file(file_name):
    # return np.genfromtxt(os.path.join(DATA_FILES_PATH,file_name), delimiter=',', dtype=int)
    return pd.read_csv(os.path.join(DATA_FILES_PATH,file_name), dtype=int)

if __name__ == '__main__':

    # save all data to CSV files
    save_all_data_to_CSVs()


    # # get data from CSV
    # dataframe = load_data_from_csv_file("x_data_window_50000.csv")
    # print(dataframe)

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