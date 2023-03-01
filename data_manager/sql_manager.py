import psycopg2
from psycopg2.extras import RealDictCursor
from data_manager import support_functions


def get_data_from_sql(commend):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute(commend)
    data = cursor.fetchall()
    return data

def insert_data_to_sql(commend):
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(commend)

def get_questions():
    commend = ("SELECT * from questions ORDER BY submision_time DESC")
    return get_data_from_sql(commend)

def get_question(id):
    commend = (f"SELECT * from questions WHERE id = {id}")
    return get_data_from_sql(commend)

def add_question(question):
    id = generate_new_id('questions')
    timestamp = support_functions.get_timestamp()
    commend = (f"INSERT into questions values({id}, '{timestamp}', 0, 0, '{question['title']}', '{question['message']}', NULL);")
    insert_data_to_sql(commend)
    return id

def generate_new_id(table):
    commend = (f"SELECT MAX(id) from {table}")
    data = get_data_from_sql(commend)
    return int(data[0]['max']) + 1

def get_answers_for_question(question_id):
    commend = (f"""SELECT id, submision_time, vote_number, message, image from answers
	WHERE question_id = {question_id}""")
    return get_data_from_sql(commend)

def add_answer(question_id, answer):
    id = generate_new_id('answers')
    timestamp = support_functions.get_timestamp()
    commend = (f"INSERT into answers values({id}, '{timestamp}', 0, {question_id}, '{answer['message']}', NULL);")
    insert_data_to_sql(commend)


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
    commend = (f"""UPDATE questions
    SET title = '{edited_data['title']}',
    message = '{edited_data['message']}'
    WHERE id = {question_id};""")
    insert_data_to_sql(commend)

def delete_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"DELETE FROM answers WHERE id = {answer_id};")
    commend3 = (f"DELETE FROM comments WHERE answer_id = {answer_id};")
    insert_data_to_sql(commend2)
    insert_data_to_sql(commend3)
    return data

def vote_up_question(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE questions
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {question_id}""")
    insert_data_to_sql(commend2)

def vote_down_question(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE questions
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {question_id}""")
    if data[0]['vote_number'] != 0:
        insert_data_to_sql(commend2)

def vote_up_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE answers
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {answer_id}""")
    insert_data_to_sql(commend2)
    return data[0]['question_id']

def vote_down_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE answers
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {answer_id}""")
    if data[0]['vote_number'] != 0:
        insert_data_to_sql(commend2)
    return data[0]['question_id']

def raise_views(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 =(f"""UPDATE questions
    SET view_number = {data[0]['view_number'] + 1}
    WHERE id = {question_id}""")
    insert_data_to_sql(commend2)

def get_question_comments(question_id):
    command = (f"""SELECT id, submision_time, message, edited_numbers from comments
    WHERE  question_id = {question_id}""")
    return get_data_from_sql(command)

def create_comment_for_question(question_id, comment):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command = (f"INSERT into comments values({id}, {question_id}, 0, '{comment['message']}', '{timestamp}', 0);")
    insert_data_to_sql(command)

def get_answer(answer_id):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command = (f"SELECT * from answers WHERE id = {answer_id}")
    return get_data_from_sql(command)

def get_answer_comments(answer_id):
    command = (f"""SELECT id, submision_time, message, edited_numbers from comments
    WHERE  answer_id = {answer_id}""")
    return get_data_from_sql(command)

def create_comment_for_answer(answer_id, comment):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command1 = (f"""SELECT * from answers
    WHERE id = {answer_id}""")
    data = get_data_from_sql(command1)
    command2 = (f"""INSERT into comments values({id}, {data[0]['question_id']}, {answer_id},
                    '{comment['message']}', '{timestamp}', 0);""")
    insert_data_to_sql(command2)

def edit_answer(answer_id, edited_data):
    command = (f"""UPDATE answers
    SET message = '{edited_data['message']}'
    WHERE id = {answer_id};""")
    insert_data_to_sql(command)

def get_comment(comment_id):
    command = (f"""SELECT * from comments
    WHERE  id = {comment_id}""")
    return get_data_from_sql(command)

def edit_comment(comment_id, edited_data):
    command1 = (f"SELECT * from comments WHERE id = {comment_id};")
    data = get_data_from_sql(command1)
    command2 = (f"""UPDATE comments
    SET message = '{edited_data['message']}',
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

def get_latest():
    command = ("""SELECT * from questions
    ORDER BY submision_time DESC
    LIMIT 5""")
    return get_data_from_sql(command)

def get_tags():
    command = ("SELECT * from tags")
    return get_data_from_sql(command)

def add_tag_to_question(tag_id, question_id):
    command = (f"INSERT into question_tags values({question_id}, {tag_id})")
    insert_data_to_sql(command)

def create_new_tag(new_tag):
    new_id = generate_new_id('tags')
    command = (f"INSERT into tags values({new_id}, '{new_tag}')")
    insert_data_to_sql(command)
    return new_id

def get_qustion_tags(question_id):
    command = (f"""SELECT * FROM question_tags
        RIGHT JOIN tags
	    ON question_tags.tag_id = tags.id
        WHERE question_id = {question_id};""")
    return get_data_from_sql(command)

def delete_question_tag(question_id, comment_id):
    command = (f"""DELETE FROM question_tags 
        WHERE question_id = {question_id} 
        AND tag_id = {comment_id}""")
    insert_data_to_sql(command)
