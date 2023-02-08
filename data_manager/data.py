import csv
from data_manager import data_const
from datetime import datetime


def read_csv():
    with open(data_const.QUESTIONS, newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def write_csv(data):
    read_data = read_csv()
    read_data.append(data)
    with open(data_const.QUESTIONS, 'w', newline='') as csvfile:
         writer = csv.writer(csvfile)
         writer.writerows(read_data)

def sort_matrix_by_column_with_headers(data,column):
    size = len(data)
    output = []
    output.append(data[0])
    while data != []:
        sorted = [0,0,0,0,0,0,0]
        most = 0 
        for i in range(1,len(data)):
            if int(data[i][column]) >= int(sorted[column]):
                sorted = data[i]
                most = i
        if len(output) == size:
            break
        output.append(sorted)
        data.remove(data[most])
    return output

def add_new_question(question_contents):
    question = []
    question.append(get_id()) 
    question.append(get_timestamp())
    question.append(0) #VIEWS NUMBER
    question.append(0) #VOTE NUMBER
    question.append(question_contents['title']) #TITLE FROM HTML
    question.append(question_contents['message']) # MESSAGE FROM HTML
    question.append('') # .jpg (TO DO LATER)
    write_csv(question)

def get_id():
    data = read_csv()
    existing_ids = [data[i][data_const.ID_POSITION] for i in range(1,len(data))]
    return (int(max(existing_ids)) + 1)

def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y%m%d%H")