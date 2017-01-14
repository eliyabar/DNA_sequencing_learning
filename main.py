from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import pandas as pd
import string
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

PCA_FEATURES=100

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

    # print(vec)

    # get the X matrix (without target) + add at begining more column for the constant
    X = data_frame.iloc[:,:-1]
    X.insert(0,'Intercept',1)
    X = X.astype(float)

    # set the target column to y
    y = np.ravel(data_frame['Category'])
    y = y.astype(float)

    # init train size
    train_size = int(len(X.index)/2)

    # print(test_size)
    # print(categories_map)

    # divide X,y for training and testing
    X_train = X.iloc[0:train_size]
    X_test = X.iloc[train_size:]
    y_train = y[0:train_size]
    y_test = y[train_size:]

    # init LogisticRegression object
    model = LogisticRegression()

    # set the model for our X and y (training)
    model = model.fit(X_train,y_train)

    # predict the answers for X_test
    predicted = model.predict(X_test)

    # compare the predict to true answers and return a accuracy score
    accuracy = metrics.accuracy_score(y_test, predicted)

    # print the result
    print("Accuracy (without PCA): %s" % accuracy)

    print("Perform PCA to original X with reduction to %s features" % PCA_FEATURES)

    # init PCA object with reduction to n_components
    pca = PCA(n_components=PCA_FEATURES)
    X_pca = pca.fit_transform(X)

    # divide X_pca for training and testing
    X_pca_train = X_pca[0:train_size]
    X_pca_test = X_pca[train_size:]

    # init LogisticRegression object
    model_pca = LogisticRegression()

    # set the model_pca for our X and y (training)
    model_pca = model_pca.fit(X_pca_train, y_train)

    # predict the answers for X_test
    predicted_pca = model_pca.predict(X_pca_test)

    # compare the predict to true answers and return a accuracy score
    accuracy_pca = metrics.accuracy_score(y_test, predicted_pca)

    # print the result
    print("Accuracy with PCA: %s" % accuracy_pca)
