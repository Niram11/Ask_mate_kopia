def list_to_dict(data, headers):
    data_list = []
    for row in data:
        data_list.append(append_new_item(row, headers))
    return data_list

def append_new_item(data_inputs, headers):
    new_data_dict = {}
    for item_index, item in enumerate(data_inputs):
        new_data_dict[headers[item_index]] = item
    return new_data_dict
    
def get_data_by_header(headers, header, data):
    data = list_to_dict(data, headers)
    return [item[header] for item in data]

def get_data_by_id(data, id):
    for row in data:
        if id in row.values():
            return row
    return []

def remove_row_from_dict(data, row):
    if row in data:
        data.remove(row)

def dict_to_list_data(data):
    data_list = []
    for row in data:
        new_row_data = []
        for value in row.values():
            new_row_data.append(value)
        data_list.append(new_row_data)
    return data_list

def add_to_file(data_inputs, headers, data):
    all_data = list_to_dict(data, headers)
    all_data.append(append_new_item(data_inputs, headers))


def return_column(data, headers, column_to_return, column_to_check, check):
    data = list_to_dict(data, headers)
    return [[row[column_to_return], row[column_to_check]] for row in data if int(row[column_to_check]) == check]

