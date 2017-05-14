
n = 10

array = [0] * n

with open("full_file.cpn", 'r') as f:
        for i, line in enumerate(f):
            index = int(float(line.split()[2])/(10))
            # print("line: " + str(i) + "  " + str(index))
            if index >= n:
                array[n-1] += 1
            else:
                array[index] += 1

print(array)