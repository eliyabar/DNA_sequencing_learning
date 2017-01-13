from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import numpy as np
import pandas as pd
import string
import math
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import collections, re
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

FILE_NAME = 'Data_tar2.csv'

def read_csv_file(file = FILE_NAME):
    if not file:
        print("No file Name")
        return
    # set of punctuations
    exclude = set(string.punctuation)

    df = pd.read_csv(file)

    df = df.FullDescription
    data_list = []
    for line in df:
        # remove punctuations
        stripped_line = ''.join(ch for ch in line if ch not in exclude)
        # lowercase line
        stripped_line = stripped_line.lower()
        # remove stopWords
        stripped_line = ' '.join([word for word in stripped_line.split() if word not in ENGLISH_STOP_WORDS])

        data_list.append(stripped_line)

    return data_list



def pca(input_mat, vars=None, num_of_reduced_features=2):
    input_mat = np.float32(input_mat)
    input_mat = np.array(input_mat);

    # subtract mean
    avg = np.mean(input_mat, axis=0)
    avg = np.tile(avg, (input_mat.shape[0], 1))
    input_mat -= avg

    # covariance matrix
    cov = np.cov(input_mat.T)
    eig_values, eig_vecs = np.linalg.eig(cov)

    idx = eig_values.argsort()
    idx = idx[::-1]
    eig_values = eig_values[idx]
    eig_vecs = eig_vecs[:, idx]

    if vars:
        var_exp = eig_values / np.sum(np.diag(cov))
        var_exp = [i for i in var_exp if i >= vars]
        eig_vecs = eig_vecs[:, :len(var_exp)]
    else:
        eig_vecs = eig_vecs[:, :num_of_reduced_features]

    # new coordinate in new space
    return np.dot(input_mat, eig_vecs).real





def extract_features(docs):
    return


# def extract_features2(data):
#     data_split = ' '.join([str(w) for doc in data for w in doc])
#     # print data_split
#     bag_of_words =  [collections.Counter(re.findall(r'\w+', txt)).most_common(10) for txt in data_split]
#     return bag_of_words



def bag_of_words(words):
    bagofwords = [collections.Counter(re.findall(r'\w+', word))for word in words]
    return  sum(bagofwords, collections.Counter())


def print_list(list):
    for line in list:
        print(line)

# Metrics
def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))

    return len(intersection) / len(union)

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude



# kmeans clustering algorithm
# data = set of data points
# k = number of clusters
# c = initial list of centroids (if provided)
#
def kmeans(data, k, max_itr):
    centroids = []

    centroids = randomize_centroids(data, centroids, k)

    old_centroids = [[] for i in range(k)]

    iterations = 0
    while (not (has_converged(centroids, old_centroids, iterations))) or iterations <= max_itr:
        iterations += 1

        clusters = [[] for i in range(k)]

        # assign data points to clusters
        clusters = euclidean_dist(data, centroids, clusters)

        # recalculate centroids
        index = 0
        for cluster in clusters:
            old_centroids[index] = centroids[index]
            centroids[index] = np.mean(cluster, axis=0).tolist()
            index += 1


    print("The total number of data instances is: " + str(len(data)))
    print("The total number of iterations necessary is: " + str(iterations))
    print("The means of each cluster are: " + str(centroids))
    print("The clusters are as follows:")
    for cluster in clusters:
        print("Cluster with a size of " + str(len(cluster)) + " starts here:")
        print(np.array(cluster).tolist())
        print("Cluster ends here.")

    return

# Calculates euclidean distance between
# a data point and all the available cluster
# centroids.
def euclidean_dist(data, centroids, clusters):
    for instance in data:
        # Find which centroid is the closest
        # to the given data point.
        mu_index = min([(i[0], np.linalg.norm(instance-centroids[i[0]])) \
                            for i in enumerate(centroids)], key=lambda t:t[1])[0]
        try:
            clusters[mu_index].append(instance)
        except KeyError:
            clusters[mu_index] = [instance]

    # If any cluster is empty then assign one point
    # from data set randomly so as to not have empty
    # clusters and 0 means.
    for cluster in clusters:
        if not cluster:
            cluster.append(data[np.random.randint(0, len(data), size=1)].flatten().tolist())

    return clusters


# randomize initial centroids
def randomize_centroids(data, centroids, k):
    for cluster in range(0, k):
        centroids.append(data[np.random.randint(0, len(data), size=1)].flatten().tolist())
    return centroids


# check if clusters have converged
def has_converged(centroids, old_centroids, iterations):
    MAX_ITERATIONS = 1000
    if iterations > MAX_ITERATIONS:
        return True
    return old_centroids == centroids


if __name__ == '__main__':
    print("--In Main--")

    full_file = read_csv_file()
    full_file = full_file[:1000]
    # print_list(full_file)

    vectorizer = CountVectorizer(max_features=200)

    # here we make this matrix with good scatter for EX
    # corraletion - when x gets bigger y gets bigger


    X = vectorizer.fit_transform(full_file).toarray()
    # np.set_printoptions(threshold=np.nan)
    # print(X[:, 0])
    # print(X)
    # print(X.shape)
    # plt.scatter(X[:, 0:22])
    # plt.axis('auto')
    # plt.show()
    # print(bag_of_words(full_file))
    # print(vectorizer.get_feature_names())

    p1 = pca(X,None, num_of_reduced_features=2)
    print(p1)
    kmeans = KMeans(n_clusters=29, random_state=0).fit(p1)
    print(kmeans.labels_)
    # pca = PCA(n_components=2)  # project from 64 to 2 dimensions
    # projected = pca.fit_transform(X)

    print("\n\n\n")
    # print(projected)



