from sklearn.linear_model import LogisticRegression
from extract_features import ExtractFeatures
from sklearn.cluster import KMeans
from prepare_data import PrepareData
import numpy as np
import pandas as pd
import timeit
import sys, os

DATA_FILES_PATH = "../DataSavedInCSV"


def save_all_data_to_CSVs():

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=500)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_1000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")
    np.savetxt(os.path.join(DATA_FILES_PATH, "y_data.csv"), y_data, delimiter=",", fmt='%10.5f', header="y", comments="")

    # data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=100)
    # x_data, y_data = data.get_matrix()
    # headers = data.get_columns_name_list()
    # np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_10000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")
    #
    # data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=10)
    # x_data, y_data = data.get_matrix()
    # headers = data.get_columns_name_list()
    # np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_1000.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")
    #
    # data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=1)
    # x_data, y_data = data.get_matrix()
    # headers = data.get_columns_name_list()
    # np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_100.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")


def load_data_from_csv_file(file_name):
    # return np.genfromtxt(os.path.join(DATA_FILES_PATH,file_name), delimiter=',', dtype=int)
    return pd.read_csv(os.path.join(DATA_FILES_PATH,file_name), dtype=int)



# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def show_menu():
    print("Please choose the menu you want to start:")
    print("1. Extract 50 features")
    print("2. Run k-means")
    print("3. Discover the main affect features")
    print("4. Run logistic Regression")
    print("5. Run logistic Regression on histograms")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    try:
        menu_actions[ch]()
    except KeyError:
        print
        "Invalid selection, please try again.\n"
        show_menu()
    return


def menu_extract_features():
    print("menu_extract_features")
    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_50000.csv")
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    logistic_object = LogisticRegression()
    logistic_object.fit(x_df, y_df)
    score = logistic_object.score(x_df, y_df)
    print("Before extract features final score: " + str(score))

    extract_df = ExtractFeatures(x_df, y_df, num_of_features=50)
    x_df_extraced_features = extract_df.get_extracted_features()

    logistic_object = LogisticRegression()
    logistic_object.fit(x_df_extraced_features, y_df)
    score = logistic_object.score(x_df_extraced_features, y_df)
    print("After extract features final score: " + str(score))


def menu_k_means():
    print("menu_k_means")
    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_50000.csv")

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(x_df)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    print(centroids)
    print(labels)


def menu_discover_affect_features():
    print("menu_discover_affect_features")
    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_50000.csv")
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    extract_df = ExtractFeatures(x_df, y_df, num_of_features=1)
    extract_df.get_extracted_features()


def menu_run_logistic():
    print("menu_run_logistic")
    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_50000.csv")
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    # logistic_object = LogisticRegression(class_weight={1: 0.9, 0: 0.1})
    logistic_object = LogisticRegression()
    logistic_object.fit(x_df, y_df)
    score = logistic_object.score(x_df, y_df)

    print("score: " + str(score))


def menu_run_logistic_on_histogram():
    print("menu_run_logistic_on_histogram")
    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_50000.csv")
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    logistic_object = LogisticRegression()
    logistic_object.fit(x_df, y_df)
    score = logistic_object.score(x_df, y_df)

    print("score: " + str(score))


# Exit program
def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    '1': menu_extract_features,
    '2': menu_k_means,
    '3': menu_discover_affect_features,
    '4': menu_run_logistic,
    '5': menu_run_logistic_on_histogram,
    '9': exit,
}

# =======================
#      MAIN PROGRAM
# =======================


if __name__ == '__main__':
    # # save all data to CSV files
    # save_all_data_to_CSVs()

    # Launch main menu
    show_menu()


