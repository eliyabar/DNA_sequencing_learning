from dir_scanner import dirScanner
import math
import numpy as np
import pandas as pd

# maximum number (of hits) that we can get in a line.
max_hits = 1000
# number of cells
n = 100
max_normalize = 3
graph_jump = 0.1
decimal_points_round = 1
arr_size = int((max_normalize / graph_jump) * 2) + 1


def open_file(path):
    with open(path, 'r') as f:
        array = [0] * n
        for i, line in enumerate(f):
            index = int(float(line.split()[2]) / (max_hits / (math.pow(10, math.log10(n)))))
            if index >= n:
                array[n - 1] += 1
            else:
                array[index] += 1
    return array[:20]


def normalize(array):
    std = np.std(array)
    mean = np.mean(array)
    for i in range(len(array)):
        normalized_num = (array[i] - mean) / std
        if normalized_num > max_normalize:
            normalized_num = max_normalize
        elif normalized_num < -max_normalize:
            normalized_num = -max_normalize

        array[i] = normalized_num

    return array


def create_index_names():
    col_names = []
    col_index = 0
    while col_index < max_hits:
        col_str = str(int(col_index)) + '_'
        col_index += (max_hits / (math.pow(10, math.log10(n))))
        col_str += str(int(col_index))
        col_names.append(col_str)
    col_names[-1] += '+'
    return list(col_names)


def create_excel_file_with_graph(data, index_names, file_name):
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame(data, index=index_names)

    # Create a Pandas Excel writer using XlsxWriter as the engine. (output.xlsx)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})

    # Configure the series of the chart from the dataframe data.
    chart.add_series({
        'values': '=Sheet1!$B$2:$B$' + str(2 + n),
        'categories': '=Sheet1!$A$2:$A$' + str(2 + n)
    })

    # Set the size of chart on sheet
    chart.set_size({'width': 1500, 'height': 700})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('D2', chart)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def all_to_one_excel_file(paths, indexes, file_name):
    print("Starting One excel file")
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    df = pd.DataFrame()
    df['index'] = indexes[:20]

    for path in paths:
        print("working on: ", path)
        normalized_array = normalize(open_file(path))
        # print(normalized_array)
        # print(path.split('\\')[-1])
        df[path.split('\\')[-1]] = normalized_array

    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    print("File ", file_name, " Saved")


# TODO : use float, cast by dtype
def normlize_vector(path):
    print("normlize_vector")

    data = pd.read_csv(path, sep="\t", header=None)[2]
    mean_val = data.mean()
    std_val = data.std()
    print("mean : ", mean_val, " std : ", std_val)
    data = data.apply(lambda row: normalize_value(row, mean_val, std_val))
    # print(data)
    return data


def normalize_value(val, mean, sdt):
    norm_val = (val - mean) / sdt
    if norm_val > max_normalize:
        norm_val = max_normalize
    elif norm_val < -max_normalize:
        norm_val = -max_normalize
    # print("val : ", val, " norm val: ", norm_val)
    return norm_val


def make_histogram_from_df(vector_df):
    histogram_arr = [0] * arr_size
    for row in vector_df:
        # graph_idx = int(round((round(row, decimal_points_round)/graph_jump), decimal_points_round))
        graph_idx = int(round(row/graph_jump, decimal_points_round))
        # print("row: ", row, " after round: ", round(row, decimal_points_round), " after div: ", round(row/graph_jump, decimal_points_round), " pre index: ", graph_idx, " make int: ", )
        # print(int(max_normalize/graph_jump) + graph_idx)
        histogram_arr[int(max_normalize / graph_jump) + graph_idx] += 1
    return histogram_arr


def make_test():
    test_data = np.arange(-max_normalize, max_normalize + graph_jump, graph_jump)
    # test_data[30] = 0
    print(test_data)
    print(make_histogram_from_df(test_data))


if __name__ == '__main__':
    # index_names = create_index_names()
    # ds = dirScanner("\\\\192.168.1.12\Public\FREEC_OUT2", "cpn")
    # normal_paths, toumor_paths = ds.get_paths()

    #  Option 1 - if we want to print each  cpn to excel file with graph.

    # for path in normal_paths:
    #     print("Working on ", path)
    #     normalized_array = normalize(open_file(path))
    #     create_excel_file_with_graph(normalized_array, index_names, path.split('\\')[-1] + ".xlsx")
    #
    # for path in toumor_paths:
    #     print("Working on ", path)
    #     normalized_array = normalize(open_file(path))
    #     create_excel_file_with_graph(normalized_array, index_names, path.split('\\')[-1] + ".xlsx")

    # Option 2 - all cpn files are in one excel file without graph
    # all_to_one_excel_file(normal_paths, index_names, "output_of_normal.xlsx")
    # all_to_one_excel_file(toumor_paths, index_names, "output_of_toumor.xlsx")

    norm_data = normlize_vector(
        "\\\\192.168.1.12\\Public\\FREEC_OUT2\\OUT_ICGC\\id_8_ICGC_normal_FI51715\window100\\ICGC_normal_FI51715.bam_sample.cpn")
    print(make_histogram_from_df(norm_data))
    print(norm_data)
    # Testings
    # make_test()
    #
    # nnnum = 1.5699878
    # print(round(nnnum, 1))
    # print(round(nnnum, 1) / graph_jump)
    #
    # print(round(nnnum / graph_jump, 1))
    # print(round((round(nnnum, 1) / graph_jump), 1))
    # print(int(round((round(nnnum, 1) / graph_jump), 1)))
