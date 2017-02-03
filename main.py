from sklearn import metrics, random_projection
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import pandas as pd
import string
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
import timeit
import os
from matplotlib import pyplot as plt

PCA_FEATURES = 100
RANDOM_PROJECTION_FEATURES = 100


def read_csv_file(file):
    # set of punctuations
    exclude = set(string.punctuation)

    df = pd.read_csv(file)

    full_desc = df.FullDescription
    data_list = []
    for line in full_desc:
        # remove punctuations
        stripped_line = ''.join(ch for ch in line if ch not in exclude)
        # lowercase line
        stripped_line = stripped_line.lower()
        # remove stopWords
        stripped_line = ' '.join([word for word in stripped_line.split() if word not in ENGLISH_STOP_WORDS])
        data_list.append(stripped_line)

    return df.iloc[:,3:5], data_list


def plot_pca_eigen_values(input_mat):
    input_mat = np.float32(input_mat)
    input_mat = np.array(input_mat)

    # subtract mean
    avg = np.mean(input_mat, axis=0)
    avg = np.tile(avg, (input_mat.shape[0], 1))
    input_mat -= avg

    # covariance matrix
    cov = np.cov(input_mat.T)
    eig_vals, eig_vecs = np.linalg.eig(cov)

    # tot = sum(eig_vals)
    # var_exp = [(i / tot) * 100 for i in sorted(eig_vals, reverse=True)]
    # cum_var_exp = np.cumsum(var_exp)
    # print(cum_var_exp)

    eig_vals = sorted(eig_vals, reverse=True)

    thefile = open('test-full-features.txt', 'w')
    for item in eig_vals:
        thefile.write("%s\n" % item)
    thefile.close()

    with plt.style.context('seaborn-whitegrid'):
        plt.figure()
        plt.bar(range(len(eig_vals)), eig_vals, alpha=0.5, align='edge',
                label='individual explained variance')
        plt.ylabel('Explained variance ratio')
        plt.xlabel('Principal components')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()




if __name__ == '__main__':
    print("--In Main--")

    # get the data as list and full file as DataFrame
    full_file, data = read_csv_file("res/Data_tar2.csv")
    file = full_file

    # extract features (vector of all the words appear in data)
    init_vec = CountVectorizer(token_pattern='\\b\\w+\\b')
    vec = init_vec.fit_transform(data).toarray()

    # convert the vector to DataFrame type
    data_frame = pd.DataFrame(vec)

    # rename the columns with the feature names
    data_frame.columns = init_vec.get_feature_names()

    # add to data_frame the target column (the Category column from csv file)
    data_frame['Category'] = file.Category

    # get all the target categories
    categories = sorted(set(data_frame['Category']))

    # create map of categories to index number
    categories_map = {k: v for v, k in enumerate(categories)}

    # print (categories_map)

    # convert the string name to index name by the map
    data_frame['Category'] = data_frame['Category'].map(categories_map)

    # get the X matrix (without target) + add at begining more column for the constant
    X = data_frame.iloc[:,:-1]
    X.insert(0,'Intercept',1)
    X = X.astype(float)

    # set the target column to y
    y = np.ravel(data_frame['Category'])
    y = y.astype(float)

    # init train size
    train_size = int(len(X.index)*0.8)

    plot_pca_eigen_values(X)

    # # divide X,y for training and testing
    # X_train = X.iloc[0:train_size]
    # X_test = X.iloc[train_size:]
    # y_train = y[0:train_size]
    # y_test = y[train_size:]
    #
    # # init start time variable for measurement time execution
    # start_time = timeit.default_timer()
    #
    # # init LogisticRegression object
    # model = LogisticRegression()
    #
    # # set the model for our X and y (training)
    # model = model.fit(X_train,y_train)
    #
    # # calculate the elapse time
    # elapsed = timeit.default_timer() - start_time
    # # print the time
    # print("Logistic Regression elapsed time: %s" % elapsed)
    #
    # # predict the answers for X_test
    # predicted = model.predict(X_test)
    #
    # # compare the predicted to true answers and return a accuracy score
    # accuracy = metrics.accuracy_score(y_test, predicted)
    #
    # # print the result
    # print("Accuracy (without dimensionality reduction): %s\n" % accuracy)
    #
    # print("Perform Random Projection to original X with reduction to %s features" % RANDOM_PROJECTION_FEATURES)
    #
    # # init start time variable for measurement time execution
    # start_time = timeit.default_timer()
    #
    # # init Random Projection object with reduction to n_components
    # random_projection = random_projection.GaussianRandomProjection(n_components=RANDOM_PROJECTION_FEATURES)
    # X_random_projection = random_projection.fit_transform(X)
    #
    # # calculate the elapsed time
    # elapsed = timeit.default_timer() - start_time
    # # print the time
    # print("Random Projection elapsed time: %s\n" % elapsed)
    #
    # # divide X_random_projection for training and testing
    # X_random_projection_train = X_random_projection[0:train_size]
    # X_random_projection_test = X_random_projection[train_size:]
    #
    # # init start time variable for measurement time execution
    # start_time = timeit.default_timer()
    #
    # # init LogisticRegression object
    # random_projection_model = LogisticRegression()
    #
    # # set the model for our X and y (training)
    # random_projection_model = random_projection_model.fit(X_random_projection_train, y_train)
    #
    # # calculate the elapse time
    # elapsed = timeit.default_timer() - start_time
    # # print the time
    # print("Logistic Regression with Random Projection elapsed time: %s" % elapsed)
    #
    # # predict the answers for X_random_projection_test
    # random_projection_predicted = random_projection_model.predict(X_random_projection_test)
    #
    # # compare the predicted data to the true answers and return an accuracy score
    # random_projection_accuracy = metrics.accuracy_score(y_test, random_projection_predicted)
    #
    # print("Accuracy with Random Projection: %s\n" % random_projection_accuracy)
    #
    # print("Perform PCA to original X with reduction to %s features" % PCA_FEATURES)
    #
    # # init start time variable for measurement time execution
    # start_time = timeit.default_timer()
    #
    # # init PCA object with reduction to n_components
    # pca = PCA(n_components=PCA_FEATURES)
    # X_pca = pca.fit_transform(X)
    #
    # # calculate the elapsed time
    # elapsed = timeit.default_timer() - start_time
    # # print the time
    # print("PCA elapsed time: %s\n" % elapsed)
    #
    # # divide X_pca for training and testing
    # X_pca_train = X_pca[0:train_size]
    # X_pca_test = X_pca[train_size:]
    #
    # # init start time variable for measurement time execution
    # start_time = timeit.default_timer()
    #
    # # init LogisticRegression object
    # pca_model = LogisticRegression()
    #
    # # set the model_pca for our X and y (training)
    # pca_model = pca_model.fit(X_pca_train, y_train)
    #
    # # calculate the elapse dtime
    # elapsed = timeit.default_timer() - start_time
    # # print the time
    # print("Logistic Regression with PCA elapsed time: %s" % elapsed)
    #
    # # predict the answers for X_pca_test
    # pca_predicted = pca_model.predict(X_pca_test)
    #
    # # compare the predicted to true answers and return a accuracy score
    # pca_accuracy = metrics.accuracy_score(y_test, pca_predicted)
    #
    # # print the result
    # print("Accuracy with PCA: %s" % pca_accuracy)
