from datetime import datetime
from data_manager import sql_manager, tags_data, user_data, questions_data, answers_data, comments_data
import hashlib

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    return str(timestamp)

def add_tag(tag, question_id):
    tags = tags_data.get_tags()
    for i in tags:
        if i['name'] == tag:
            tags_data.add_tag_to_question(i['id'], question_id)
            return
    new_tag_id = tags_data.create_new_tag(tag)
    tags_data.add_tag_to_question(new_tag_id, question_id)

def secure_password(password):
    password = generate_soil(password)
    password = password.encode()
    return hashlib.sha512(password).hexdigest()

#TODO wprowadzenie rzeczywistego generowania soli lub zmiana algorytmu
def generate_soil(password):
    password = password + password
    return password

def login(login_data):
    password = secure_password(login_data['password'])
    stored_password = user_data.check_password(login_data['username'])
    if user_data.check_for_existing_user(login_data['username']) and (password == stored_password):
        print('logged')
        return True
    else:
        print('incorect')
        return False
    
def get_user_entries(username):
    questions = questions_data.get_user_questions(username)
    answers = answers_data.get_user_answers(username)
    comments = comments_data.get_user_comments(username)
    return questions, answers, comments
