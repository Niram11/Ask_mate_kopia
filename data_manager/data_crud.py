from data_manager import data_functions, connection
from exceptions import DeleteException


def read_data(datafile, headers=''):
    data = connection.read_table_from_file(datafile)
    return data


def add_data(datafile, headers, data_inputs):
    data = connection.read_table_from_file(datafile)
    data = data_functions.list_to_dict(data, headers)
    data.append(data_functions.append_new_item(data_inputs, headers))
    data_table = data_functions.dict_to_list_data(data)
    connection.write_table_to_file(datafile, data_table)


def update_data(datafile, headers, data_inputs):
    add_data(datafile, headers, data_inputs)


def remove_data(datafile, headers, id):
    data = connection.read_table_from_file(datafile)
    data = data_functions.list_to_dict(data, headers)
    row_with_id = data_functions.get_data_by_id(data, id)
    if row_with_id == []:
        raise DeleteException
    data_functions.remove_row_from_dict(data, row_with_id)
    data_table = data_functions.dict_to_list_data(data)
    connection.write_table_to_file(datafile, data_table)
