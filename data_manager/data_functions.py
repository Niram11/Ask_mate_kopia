import csv
from data_manager import data_const


def read_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data


def write_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def get_ids(data):
    output = [data[i][data_const.ID_POSITION] for i in range(1, len(data))]
    return output


def get_submission_time(data):
    output = [data[i][data_const.SUBMIOSION_TIME_POSITION] for i in range(1, len(data))]
    return output


def get_view_number(data):
    output = [data[i][data_const.VIEW_NUMBER_POSITION] for i in range(1, len(data))]
    return output


def get_vote_number(data):
    output = [data[i][data_const.VOTE_NUMBER_POSITION] for i in range(1, len(data))]
    return output


def get_title(data):
    output = [data[i][data_const.TITLE_POSITION] for i in range(1, len(data))]
    return output


def get_message(data):
    output = [data[i][data_const.MESSAGE_POSITION] for i in range(1, len(data))]
    return output


def get_single_id(data):
    return data[0]


def get_answers_with_question_id(data):
    list_answers = []
    for value in enumerate(data):
        list_answers.append(value)
    return list_answers


def sort_matrix_by_column_with_headers(data, column):
    output = [data[0]]
    data.remove(data[0])
    while data != []:
        sorted = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(data)):
            if int(data[i][column]) >= int(sorted[column]):
                sorted = data[i]
                most = i
        output.append(sorted)
        data.remove(data[most])
    return output


def get_data_with_id_and_headers(data, id):
    headers = data[0]
    data_with_id = [data[i] for i in range(len(data)) if data[i][0] == id]
    data_with_id.insert(0, headers)
    return data_with_id


def get_question_with_id(data, id):
    question_with_id = [data[i] for i in range(len(data)) if data[i][0] == id]
    return question_with_id[0]


def edit_data_with_id(all_data, id, edited_question):
    place = 0
    for i in range(len(all_data)):
        if all_data[i][0] == id:
            place = i
    all_data[place][data_const.TITLE_POSITION] = edited_question['title']
    all_data[place][data_const.MESSAGE_POSITION] = edited_question['message']
    write_csv(all_data, data_const.QUESTIONS)

    # size = len(data)
    # output = []
    # output.append(data[0])
    # while data != []:
    #     sorted = [0,0,0,0,0,0,0]
    #     most = 0 
    #     for i in range(1,len(data)):
    #         if int(data[i][column]) >= int(sorted[column]):
    #             sorted = data[i]
    #             most = i
    #     if len(output) == size:
    #         break
    #     output.append(sorted)
    #     data.remove(data[most])
    # return output

# def list_to_dict(data, headers):
#     data_list = []
#     for row in data:
#         data_list.append(append_new_item(row, headers))
#     return data_list

# def append_new_item(data_inputs, headers):
#     new_data_dict = {}
#     for item_index, item in enumerate(data_inputs):
#         new_data_dict[headers[item_index]] = item
#     return new_data_dict

# def get_data_by_header(headers, header, data):
#     data = list_to_dict(data, headers)
#     return [item[header] for item in data]

# def get_data_by_id(data, id):
#     for row in data:
#         if id in row.values():
#             return row
#     return []

# def remove_row_from_dict(data, row):
#     if row in data:
#         data.remove(row)

# def dict_to_list_data(data):
#     data_list = []
#     for row in data:
#         new_row_data = []
#         for value in row.values():
#             new_row_data.append(value)
#         data_list.append(new_row_data)
#     return data_list

# def add_to_file(data_inputs, headers, data):
#     all_data = list_to_dict(data, headers)
#     all_data.append(append_new_item(data_inputs, headers))


# def return_column(data, headers, column_to_return, column_to_check, check):
#     data = list_to_dict(data, headers)
#     return [[row[column_to_return], row[column_to_check]] for row in data if int(row[column_to_check]) == check]
