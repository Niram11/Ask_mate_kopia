from data_manager import data_functions
from datetime import datetime


def write_new_question(data, filename):
    read_data = data_functions.read_csv(filename)
    read_data.append(data)
    data_functions.write_csv(read_data, filename)

def add_new_question(question_contents, filename):
    question = []
    question.append(get_id(filename)) 
    question.append(get_timestamp())
    question.append(0) #VIEWS NUMBER
    question.append(0) #VOTE NUMBER
    question.append(question_contents['title']) #TITLE FROM HTML
    question.append(question_contents['message']) # MESSAGE FROM HTML
    question.append('') # .jpg (TO DO LATER)
    write_new_question(question, filename)
    return data_functions.get_single_id(question)

def get_id(filename):
    data = data_functions.read_csv(filename)
    existing_ids = data_functions.get_ids(data)
    return (int(max(existing_ids)) + 1)

def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y%m%d%H")