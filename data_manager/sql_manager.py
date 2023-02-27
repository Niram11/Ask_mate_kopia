import psycopg2
from psycopg2.extras import RealDictCursor
from data_manager import support_functions

def get_questions():
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("""SELECT * from questions
    ORDER BY submision_time DESC""")
    data = cursor.fetchall()
    return data

def get_question(id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from questions WHERE id = {id}")
    data = cursor.fetchall()
    return data

def add_question(question):
    id = generate_new_id('questions')
    timestamp = support_functions.get_timestamp()
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"INSERT into questions values({id}, '{timestamp}', 0, 0, '{question['title']}', '{question['message']}', NULL);")
    return id

def generate_new_id(table):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT MAX(id) from {table}")
    data = cursor.fetchall()
    return int(data[0]['max']) + 1

def get_answers_for_question(question_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"""SELECT id, submision_time, vote_number, message, image from answers
	WHERE question_id = {question_id}""")
    data = cursor.fetchall()
    return data

def add_answer(question_id,answer):
    id = generate_new_id('answers')
    timestamp = support_functions.get_timestamp()
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"INSERT into answers values({id}, '{timestamp}', 0, {question_id}, '{answer['message']}', NULL);")

def delete_question(question_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM questions WHERE id = {question_id};")
    cursor.execute(f"DELETE FROM answers WHERE question_id = {question_id};")

def edit_question(question_id, edited_data):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE questions
    SET title = '{edited_data['title']}',
    message = '{edited_data['message']}'
    WHERE id = {question_id};""")

def delete_answer(answer_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from answers WHERE id = {answer_id};")
    data = cursor.fetchall()
    cursor.execute(f"DELETE FROM answers WHERE id = {answer_id};")
    return data

def vote_up_question(question_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from questions WHERE id = {question_id};")
    data = cursor.fetchall()
    cursor.execute(f"""UPDATE questions
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {question_id}""")

def vote_down_question(question_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from questions WHERE id = {question_id};")
    data = cursor.fetchall()
    if data[0]['vote_number'] != 0:
        cursor.execute(f"""UPDATE questions
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {question_id}""")

def vote_up_answer(answer_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from answers WHERE id = {answer_id};")
    data = cursor.fetchall()
    cursor.execute(f"""UPDATE answers
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {answer_id}""")
    return data[0]['question_id']

def vote_down_answer(answer_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from answers WHERE id = {answer_id};")
    data = cursor.fetchall()
    if data[0]['vote_number'] != 0:
        cursor.execute(f"""UPDATE answers
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {answer_id}""")
    return data[0]['question_id']

def raise_views(question_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from questions WHERE id = {question_id};")
    data = cursor.fetchall()
    cursor.execute(f"""UPDATE questions
    SET view_number = {data[0]['view_number'] + 1}
    WHERE id = {question_id}""")

def get_question_comments(question_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"""SELECT id, submision_time, message, edited_numbers from comments
    WHERE  question_id = {question_id}""")
    data = cursor.fetchall()
    return data

def create_comment_for_question(question_id, comment):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"INSERT into comments values({id}, {question_id}, 0, '{comment['message']}', '{timestamp}', 0);")

def get_answer(answer_id):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from answers WHERE id = {answer_id}")
    data = cursor.fetchall()
    return data

def get_answer_comments(answer_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"""SELECT id, submision_time, message, edited_numbers from comments
    WHERE  answer_id = {answer_id}""")
    data = cursor.fetchall()
    return data

def create_comment_for_answer(answer_id, comment):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"INSERT into comments values({id}, 0, {answer_id}, '{comment['message']}', '{timestamp}', 0);")

def edit_answer(answer_id, edited_data):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE answers
    SET message = '{edited_data['message']}'
    WHERE id = {answer_id};""")

def get_comment(comment_id):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"""SELECT * from comments
    WHERE  id = {comment_id}""")
    data = cursor.fetchall()
    return data

def edit_comment(comment_id, edited_data):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(f"SELECT * from comments WHERE id = {comment_id};")
    data = cursor.fetchall()
    cursor.execute(f"""UPDATE comments
    SET message = '{edited_data['message']}',
    edited_numbers = {data[0]['edited_numbers'] + 1}
    WHERE id = {comment_id};""")