from data_manager.sql_manager import get_data_from_sql, insert_data_to_sql
from data_manager import support_functions, sql_manager

def get_question_comments(question_id):
    command = (f"""SELECT id, submision_time, message, edited_numbers, username from comments
    WHERE  question_id = {question_id} and answer_id = 0""")
    return get_data_from_sql(command)

def create_comment_for_question(question_id, comment):
    id = sql_manager.generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    message = sql_manager.clear_inputs(comment['message'])
    command = (f"INSERT into comments values({id}, {question_id}, 0, '{message}', '{timestamp}', 0, '{comment['username']}');")
    insert_data_to_sql(command)

def get_answer_comments(answer_id):
    command = (f"""SELECT id, submision_time, message, edited_numbers, username from comments
    WHERE  answer_id = {answer_id}""")
    return get_data_from_sql(command)

def create_comment_for_answer(answer_id, comment):
    id = sql_manager.generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command1 = (f"""SELECT * from answers
    WHERE id = {answer_id}""")
    message = sql_manager.clear_inputs(comment['message'])
    data = get_data_from_sql(command1)
    command2 = (f"""INSERT into comments values({id}, {data[0]['question_id']}, {answer_id},
                    '{message}', '{timestamp}', 0, '{comment['username']}');""")
    insert_data_to_sql(command2)


def get_comment(comment_id):
    command = (f"""SELECT * from comments
    WHERE  id = {comment_id}""")
    return get_data_from_sql(command)

def edit_comment(comment_id, edited_data):
    command1 = (f"SELECT * from comments WHERE id = {comment_id};")
    data = get_data_from_sql(command1)
    message = sql_manager.clear_inputs(edited_data['message'])
    command2 = (f"""UPDATE comments
    SET message = '{message}',
    edited_numbers = {data[0]['edited_numbers'] + 1}
    WHERE id = {comment_id};""")
    insert_data_to_sql(command2)

def delete_question_comment(comment_id):
    command1 = (f"SELECT * from comments WHERE id = {comment_id};")
    data = get_data_from_sql(command1)
    command2 = (f"DELETE FROM comments WHERE id = {comment_id};")
    insert_data_to_sql(command2)
    return data[0]['question_id']

def delete_answer_comment(comment_id):
    command1 = (f"SELECT * from comments WHERE id = {comment_id};")
    data = get_data_from_sql(command1)
    command2 = (f"DELETE FROM comments WHERE id = {comment_id};")
    insert_data_to_sql(command2)
    return data[0]['answer_id']


def get_user_comments(username):
    commend = (f"""SELECT * from comments 
                WHERE username = '{username}'
               ORDER BY submision_time DESC""")
    return get_data_from_sql(commend)


