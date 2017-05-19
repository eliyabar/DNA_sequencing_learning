from dir_scanner import dirScanner
import numpy as np


class PrepareData:

    WINDOW_SIZE = 100
    ORIGINAL_VECTOR_LENGTH = 30956785

    def __init__(self, path_to_data, union_window_number=1):
        self._path = path_to_data
        self._union_win_number = union_window_number
        self._columns_base_name = union_window_number * self.WINDOW_SIZE
        self._vector_length = np.math.ceil(self.ORIGINAL_VECTOR_LENGTH / union_window_number)
        ds = dirScanner(path_to_data, "cpn")
        self._normal_paths, self._tumor_paths = ds.get_paths()
        self._columns_name_list = self._create_columns_name_list()
        print("init finished")

    def _create_columns_name_list(self):
        columns_name = ""
        for index in range(self._vector_length):
            columns_name += str(index*self._columns_base_name) + "_" + str((index+1)*self._columns_base_name) + ","
        return columns_name[:-1]

    def _get_value_list(self, path):
        value_list = []
        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                value = int(line.split("\t")[-1])
                value_list.append(value)
        if self._union_win_number > 1:
            return np.add.reduceat(value_list, np.arange(0, len(value_list), self._union_win_number))
        else:
            return value_list

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