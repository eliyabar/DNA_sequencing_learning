from sklearn.linear_model import LogisticRegression
from extract_features import ExtractFeatures
from sklearn.cluster import KMeans
from prepare_data import PrepareData
import numpy as np
import pandas as pd
from sklearn import metrics
import timeit
import sys, os

DATA_FILES_PATH = "../DataSavedInCSV"


def save_all_data_to_CSVs():

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=500)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_50000_normalized.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")
    np.savetxt(os.path.join(DATA_FILES_PATH, "y_data.csv"), y_data, delimiter=",", fmt='%10.5f', header="y", comments="")

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=100)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_10000_normalized.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")

    data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=10)
    x_data, y_data = data.get_matrix()
    headers = data.get_columns_name_list()
    np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_1000_normalized.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")

    # data = PrepareData("D:\FinalProject\FREEC_OUT2", union_window_number=1)
    # x_data, y_data = data.get_matrix()
    # headers = data.get_columns_name_list()
    # np.savetxt(os.path.join(DATA_FILES_PATH, "x_data_window_100.csv"), x_data, delimiter=",", fmt='%10.5f', header=headers, comments="")


def load_data_from_csv_file(file_name, dtype=int):
    # return np.genfromtxt(os.path.join(DATA_FILES_PATH,file_name), delimiter=',', dtype=int)
    return pd.read_csv(os.path.join(DATA_FILES_PATH,file_name), dtype=dtype)



# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def show_menu():
    print("Please choose the menu you want to start:")
    print("1. Extract 50 features")
    print("2. Run k-means")
    print("3. Discover the main affect features")
    print("4. Run Logistic Regression")
    print("5. Run Logistic Regression on histograms")
    print("6. Run Logistic Regression with 80% train and 20% test")
    print("8. Save to files")
    print("9. Exit")
    choice = input(" >>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    try:
        menu_actions[ch]()
    except KeyError:
        print("Invalid selection, please try again.\n")
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
    x_df = load_data_from_csv_file("x_data_histograms.csv", dtype=float)
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    logistic_object = LogisticRegression()
    logistic_object.fit(x_df, y_df)
    score = logistic_object.score(x_df, y_df)

    print("score: " + str(score))


def menu_run_logistic_train_and_test():
    print("menu_run_logistic")
    # get data from CSV
    x_df = load_data_from_csv_file("x_data_window_50000.csv")
    y_df = np.ravel(load_data_from_csv_file("y_data.csv"))

    sample_weigth = [10, 10, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # init train size
    train_size = int(len(x_df.index) * 0.8)

    X_train = x_df.iloc[0:train_size]
    X_test = x_df.iloc[train_size:]
    y_train = y_df[0:train_size]
    y_test = y_df[train_size:]

    sample_weigth_train = sample_weigth[0:train_size]
    sample_weigth_test = sample_weigth[train_size:]


    logistic_object = LogisticRegression(solver='lbfgs')
    logistic_object.fit(X_train, y_train, sample_weight=sample_weigth_train)
    score = logistic_object.score(X_train, y_train, sample_weight=sample_weigth_train)
    print("Training score: " + str(score))

    # # predict the answers for X_test
    # predicted = logistic_object.predict(X_test)
    #
    # # compare the predicted to true answers and return a accuracy score
    # accuracy = metrics.accuracy_score(y_test, predicted)
    accuracy = logistic_object.score(X_test, y_test, sample_weight=sample_weigth_test)
    print("Testing score: " + str(accuracy))



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
    '6': menu_run_logistic_train_and_test,
    '8': save_all_data_to_CSVs,
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


