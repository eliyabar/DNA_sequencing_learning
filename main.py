from patsy.highlevel import dmatrices
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import pandas as pd
import string
import math
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression


def read_csv_file(file=None):
    if not file:
        print("No file Name")
        return
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

def print_list(list):
    for line in list:
        print(line)


class LogisticReg(object):
    pass


if __name__ == '__main__':
    print("--In Main--")

    full_file, data = read_csv_file("res/Data_tar2.csv")
    file = full_file

    init_vec = CountVectorizer(token_pattern='\\b\\w+\\b')
    vec = init_vec.fit_transform(data).toarray()

    # print(init_vec.get_feature_names())
    vec = pd.DataFrame(vec)
    vec.columns = init_vec.get_feature_names()
    vec['Category'] = file.Category

    categories = sorted(set(vec['Category']))
    categories_map = {k: v for v, k in enumerate(categories)}
    # print (categories_map)
    vec['Category'] =vec['Category'].map(categories_map)
    # print(vec)

    format = 'Category ~ '
    for col in init_vec.get_feature_names():
        format += "%s + " % col
    format = format[:-3]
    # print(format)
    # y, X = dmatrices(format, vec, return_type="dataframe")

    X = vec.iloc[:,:-1]
    X.insert(0,'Intercept',1)
    X = X.astype(float)

    y = np.ravel(vec['Category'])
    y = y.astype(float)




    # X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.5, random_state=1)
    # print(X_train)

    test_size =int(len(X.index)/2)
    # print(test_size)
    # print(categories_map)

    X_train = X.iloc[0:test_size]
    X_test = X.iloc[test_size:]

    y_train = y[0:test_size]
    y_test = y[test_size:]


    model = LogisticRegression()
    model = model.fit(X_train,y_train)

    predicted = model.predict(X_test)
    print(predicted)

    accuracy = metrics.accuracy_score(y_test, predicted)
    print("Regular accuracy: %s" % accuracy)






    pca = PCA(n_components=2)  # project from 64 to 2 dimensions
    X_pca = pca.fit_transform(X)

    X_pca_train = X_pca.iloc[0:test_size]
    X_pca_test = X_pca.iloc[test_size:]

    model_pca = LogisticRegression()
    model_pca = model_pca.fit(X_pca_train, y_train)

    predicted_pca = model_pca.predict(X_pca_test)
    print(predicted_pca)

    accuracy_pca = metrics.accuracy_score(y_test, predicted_pca)
    print("pca accuracy: %s" % accuracy_pca)
