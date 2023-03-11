from datetime import datetime
from data_manager import sql_manager
import hashlib

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    return str(timestamp)

def add_tag(tag, question_id):
    tags = sql_manager.get_tags()
    for i in tags:
        if i['name'] == tag:
            sql_manager.add_tag_to_question(i['id'], question_id)
            return
    new_tag_id = sql_manager.create_new_tag(tag)
    sql_manager.add_tag_to_question(new_tag_id, question_id)

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
    stored_password = sql_manager.check_password(login_data['username'])
    if sql_manager.check_for_existing_user(login_data['username']) and (password == stored_password):
        print('logged')
        return True
    else:
        print('incorect')
        return False
    
def get_user_entries(username):
    questions = sql_manager.get_user_questions(username)
    answers = sql_manager.get_user_answers(username)
    comments = sql_manager.get_user_comments(username)
    return questions, answers, comments
