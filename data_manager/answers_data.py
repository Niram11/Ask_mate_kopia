from data_manager.sql_manager import get_data_from_sql, insert_data_to_sql
from data_manager import support_functions, sql_manager

def get_answers_for_question(question_id):
    commend = (f"""SELECT id, submision_time, vote_number, message, image, username, accept_status from answers
	WHERE question_id = {question_id}""")
    return get_data_from_sql(commend)

def add_answer(question_id, answer):
    id = sql_manager.generate_new_id('answers')
    timestamp = support_functions.get_timestamp()
    message = sql_manager.clear_inputs(answer['message'])
    commend = (f"""INSERT into answers values({id}, '{timestamp}', 0, {question_id}, 
                '{message}', NULL, '{answer['username']}');""")
    insert_data_to_sql(commend)

def delete_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"DELETE FROM answers WHERE id = {answer_id};")
    commend3 = (f"DELETE FROM comments WHERE answer_id = {answer_id};")
    insert_data_to_sql(commend2)
    insert_data_to_sql(commend3)
    return data

def get_answer(answer_id):
    command = (f"SELECT * from answers WHERE id = {answer_id}")
    return get_data_from_sql(command)


def edit_answer(answer_id, edited_data):
    message = sql_manager.clear_inputs(edited_data['message'])
    command = (f"""UPDATE answers
    SET message = '{message}'
    WHERE id = {answer_id};""")
    insert_data_to_sql(command)

def get_user_answers(username):
    commend = (f"""SELECT * from answers
                WHERE username = '{username}'
               ORDER BY submision_time DESC""")
    return get_data_from_sql(commend)

def accept_answer(answer_id):
    command2 = (f"SELECT * from answers WHERE id = {answer_id}")
    answer_data = get_data_from_sql(command2)
    command = (f"""UPDATE answers
    SET accept_status = 'accepted'
    WHERE id = {answer_id};""")
    insert_data_to_sql(command)
    sql_manager.increase_reputation(answer_data[0]['username'], 15)
    return answer_data[0]['question_id']


def unaccept_answer(answer_id):
    command2 = (f"SELECT * from answers WHERE id = {answer_id}")
    answer_data = get_data_from_sql(command2)
    command = (f"""UPDATE answers
    SET accept_status = NULL
    WHERE id = {answer_id};""")
    insert_data_to_sql(command)
    sql_manager.decrease_reputation(answer_data[0]['username'], 15)
    return answer_data[0]['question_id']