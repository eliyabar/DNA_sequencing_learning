# max_score -> 0.000000.....
# num of feature -> 30 million - maybe long?!
from sklearn.linear_model import LogisticRegression


class ExtractFeatures:
    def __init__(self, x_data, y_data, num_of_features=50):
        self._x_data = x_data
        self._y_data = y_data
        self._num_of_features = num_of_features
        self.extract_features()

    def extract_features(self):
        i = 0
        self._all_features = list(self._x_data)
        print(self._all_features)
        self._selected_features = []
        logistic_object = LogisticRegression()

        while i < self._num_of_features:
            tested_features = list(set(self._all_features) - set(self._selected_features))
            max_score = 0
            selected_feature = None
            for feature in tested_features:
                temp_selected_features = list(self._selected_features)
                temp_selected_features.append(feature)
                temp_x_df = self._x_data[temp_selected_features].copy()
                # print(temp_x_df)
                logistic_object.fit(temp_x_df, self._y_data)
                score = logistic_object.score(temp_x_df, self._y_data)
                # print("score: " + str(score))
                if score > max_score:
                    max_score = score
                    selected_feature = feature

            self._selected_features.append(selected_feature)
            print("finish: ", self._selected_features)
            i += 1
