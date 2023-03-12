from data_manager.sql_manager import get_data_from_sql, insert_data_to_sql
from data_manager import support_functions, sql_manager

def get_questions():
    commend = ("SELECT * from questions ORDER BY submision_time DESC")
    return get_data_from_sql(commend)

def get_question(id):
    commend = (f"SELECT * from questions WHERE id = {id}")
    return get_data_from_sql(commend)

def add_question(question):
    id = sql_manager.generate_new_id('questions')
    timestamp = support_functions.get_timestamp()
    title = sql_manager.clear_inputs(question['title'])
    message = sql_manager.clear_inputs(question['message'])
    commend = (f"""INSERT into questions values({id}, '{timestamp}', 0, 0, '{title}',
                '{message}', NULL, '{question['username']}');""")
    insert_data_to_sql(commend)
    return id

def delete_question(question_id):
    commend1 = (f"DELETE FROM questions WHERE id = {question_id};")
    commend2 = (f"DELETE FROM answers WHERE question_id = {question_id};")
    commend3 = (f"DELETE FROM comments WHERE question_id = {question_id};")
    commend4 = (f"DELETE FROM question_tags WHERE question_id = {question_id}")
    insert_data_to_sql(commend1)
    insert_data_to_sql(commend2)
    insert_data_to_sql(commend3)
    insert_data_to_sql(commend4)

def edit_question(question_id, edited_data):
    title = sql_manager.clear_inputs(edited_data['title'])
    message = sql_manager.clear_inputs(edited_data['message'])
    commend = (f"""UPDATE questions
    SET title = '{title}',
    message = '{message}'
    WHERE id = {question_id};""")
    insert_data_to_sql(commend)

def get_latest():
    command = ("""SELECT * from questions
    ORDER BY submision_time DESC
    LIMIT 5""")
    return get_data_from_sql(command)

def search_in_questions(search):
    search = sql_manager.clear_inputs(search)
    command = (f"""SELECT * from questions
        WHERE title LIKE '%{search}%'
        OR message LIKE '%{search}%'""")
    return get_data_from_sql(command)


def get_sorted_questions(order_by, order_direction):
    commend = (f"""SELECT * from questions
        ORDER BY {order_by} {order_direction}""")
    return get_data_from_sql(commend)

def get_user_questions(username):
    commend = (f"""SELECT * from questions 
                WHERE username = '{username}'
               ORDER BY submision_time DESC""")
    return get_data_from_sql(commend)

