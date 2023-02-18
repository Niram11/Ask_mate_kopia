from data_manager import data_functions, data_const
from datetime import datetime


def write_new_data(data, filename):
    read_data = data_functions.read_csv(filename)
    read_data.append(data)
    data_functions.write_csv(read_data, filename)


def add_new_question(question_contents, filename):
    question = []
    question.append(get_id(filename))
    question.append(get_timestamp())
    question.append(0)  # VIEWS NUMBER
    question.append(0)  # VOTE NUMBER
    question.append(question_contents['title'])  # TITLE FROM HTML
    question.append(question_contents['message'])  # MESSAGE FROM HTML
    question.append('')  # .jpg (TO DO LATER)
    write_new_data(question, filename)
    return data_functions.get_single_id(question)


def get_id(filename):
    data = data_functions.read_csv(filename)
    existing_ids = data_functions.get_ids(data)
    return int(max(existing_ids)) + 1


def add_new_answer(answer_content, filename, question_id):
    answers = []
    answers.append(get_id(filename))
    answers.append(get_timestamp())
    answers.append(0)  # vote
    answers.append(question_id)
    answers.append(answer_content['message'])
    answers.append('')  # image
    write_new_data(answers, filename)


def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y%m%d%H")


def delete_question_with_id(data, question_id):
    question = data_functions.get_question_with_id(data, question_id)
    data.remove(question)
    data_functions.write_csv(data, data_const.QUESTIONS)
