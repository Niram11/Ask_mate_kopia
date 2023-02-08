import csv


def read_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def sort_matrix_by_column_with_headers(data,column):
    size = len(data)
    output = []
    output.append(data[0])
    while data != []:
        sorted = [0,0,0,0,0,0,0]
        most = 0 
        for i in range(1,len(data)):
            if int(data[i][column]) > int(sorted[column]):
                sorted = data[i]
                most = i
        if len(output) == size:
            break
        output.append(sorted)
        data.remove(data[most])
    return output
