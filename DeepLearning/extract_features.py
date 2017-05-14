# max_score -> 0.000000.....
# num of feature -> 30 million - maybe long?!


class ExtractFeatures:
    def __init__(self, data_matrix, num_of_features=50):
        self._data_matrix = data_matrix
        self._num_of_features = num_of_features
        self.extract_features()

    def extract_features(self):
        i = 0
        self._all_features = list(self._data_matrix)
        self._selected_features = []

        while i < self._num_of_features:
            tested_features = list(set(self._all_features) - set(self._selected_features))
            max_score = 0
            selected_feature = None

            for feature in tested_features:
                temp_selected_features = list(self._selected_features)
                temp_selected_features.append(feature)
                print(temp_selected_features)

                # train with temp_selected_features
                # will be the max from the learning
                max_score = 4
                selected_feature = feature

            self._selected_features.append(selected_feature)
            print("finish: ", self._selected_features)
            i += 1
