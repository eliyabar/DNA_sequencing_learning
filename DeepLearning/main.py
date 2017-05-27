from sklearn.linear_model import LogisticRegression
from extract_features import ExtractFeatures
from prepare_data import PrepareData
import numpy as np
import os
import pandas as pd
import timeit

DATA_FILES_PATH = "../DataSavedInCSV"


def save_all_data_to_CSVs():

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=500)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_50000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")
    np.savetxt(os.path.join(DATA_FILES_PATH, "y_data.csv"), y_data, delimiter=",", fmt='%10.5f', header="y", comments="")

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=100)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_10000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=10)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_1000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=1)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_100.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")


def load_data_from_csv_file(file_name):
    # return np.genfromtxt(os.path.join(DATA_FILES_PATH,file_name), delimiter=',', dtype=int)
    return pd.read_csv(os.path.join(DATA_FILES_PATH,file_name), dtype=int)

if __name__ == '__main__':

    # # save all data to CSV files
    # save_all_data_to_CSVs()

    # init start time variable for measurement time execution
    start_time = timeit.default_timer()

    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_100.csv")
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    # calculate the elapsed time
    elapsed = timeit.default_timer() - start_time
    print("load data from csv file: %s\n" % elapsed)

    x_df = x_df.iloc[:, :10]
    print(x_df)

    # extract = ExtractFeatures(x_df, y_df, num_of_features=10)