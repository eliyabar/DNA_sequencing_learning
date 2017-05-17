from dir_scanner import dirScanner
import math
import numpy as np
import pandas as pd


# maximum number (of hits) that we can get in a line.
max_hits = 1000
# number of cells
n = 100
max_normalize = 3


def open_file(path):
    with open(path, 'r') as f:
        array = [0] * n
        for i, line in enumerate(f):
            index = int(float(line.split()[2]) / (max_hits / (math.pow(10, math.log10(n)))))
            # print("line: " + str(i) + "  " + str(index))
            if index >= n:
                array[n - 1] += 1
            else:
                array[index] += 1
    return array


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
    workbook  = writer.book
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




if __name__ == '__main__':

    normalized_array = normalize(open_file("full_file.cpn"))
    print("Normalized Array:\n", normalized_array)

    index_names = create_index_names()

    create_excel_file_with_graph(normalized_array, index_names, "output.xlsx")

