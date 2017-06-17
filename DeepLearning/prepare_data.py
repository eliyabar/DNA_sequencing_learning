from dir_scanner import dirScanner
import numpy as np
import warnings


class PrepareData:

    WINDOW_SIZE = 100
    ORIGINAL_VECTOR_LENGTH = 30956785
    NORMALIZE_CONSTANT = 3

    def __init__(self, path_to_data, union_window_number=1):
        self._path = path_to_data
        self._union_win_number = union_window_number
        self._columns_base_name = union_window_number * self.WINDOW_SIZE
        self._vector_length = np.math.ceil(self.ORIGINAL_VECTOR_LENGTH / union_window_number)
        ds = dirScanner(path_to_data, "cpn")
        self._normal_paths, self._tumor_paths = ds.get_paths()
        # self._columns_name_list = self._create_columns_name_list()
        self._columns_name_list = ""
        print("init finished")

    def _create_columns_name_list(self):
        columns_name = ""
        for index in range(self._vector_length):
            columns_name += str(index*self._columns_base_name) + "_" + str((index+1)*self._columns_base_name) + ","
        return columns_name[:-1]

    def _normalize_vector(self, array):
        normalized_array = [None]*len(array)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            std = np.std(array)
            mean = np.mean(array)
        for i in range(len(array)):
            normalized_num = (array[i] - mean) / std
            if normalized_num > self.NORMALIZE_CONSTANT:
                normalized_num = self.NORMALIZE_CONSTANT
            elif normalized_num < -self.NORMALIZE_CONSTANT:
                normalized_num = -self.NORMALIZE_CONSTANT
            normalized_array[i] = normalized_num

        return normalized_array

    def _get_value_list(self, path):
        value_list = []
        temp_list = []
        columns_name = ""
        current_chromosome = '1'
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                lines_values = line.split("\t")
                chromosome = lines_values[0]
                value = int(lines_values[-1])
                if chromosome == current_chromosome:
                    temp_list.append(value)
                    last_position = lines_values[1]
                else:
                    temp_list = np.add.reduceat(temp_list, np.arange(0, len(temp_list), self._union_win_number))
                    last = len(temp_list) - 1
                    for index, temp in enumerate(temp_list):
                        value_list.append(temp)
                        if index == last:
                            end_pos = last_position
                        else:
                            end_pos = str((index+1)*self._columns_base_name)
                        columns_name += current_chromosome + "_" + str(index*self._columns_base_name) + "_" + end_pos + ","
                    temp_list = []
                    temp_list.append(value)
                    current_chromosome = chromosome
        self._columns_name_list = columns_name[:-1]
        return self._normalize_vector(value_list)

    def get_matrix(self):
        x_matrix = []
        y = []
        for path in self._normal_paths:
            value_list = self._get_value_list(path)
            if len(value_list) > 0:
                x_matrix.append(value_list)
                y.append(1)

        for path in self._tumor_paths:
            value_list = self._get_value_list(path)
            if len(value_list) > 0:
                x_matrix.append(value_list)
                y.append(0)

        return np.asarray(x_matrix), np.asarray(y)

    def get_columns_name_list(self):
        return self._columns_name_list