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
    commend = (f"""INSERT into questions values({id}, '{timestamp}', 0, 0, '{question['title']}',
                '{question['message']}', NULL, '{question['username']}');""")
    insert_data_to_sql(commend)
    return id

def generate_new_id(table):
    try:
        commend = (f"SELECT MAX(id) from {table}")
        data = get_data_from_sql(commend)
        return int(data[0]['max']) + 1
    except:
        return 1

def get_answers_for_question(question_id):
    commend = (f"""SELECT id, submision_time, vote_number, message, image, username, accept_status from answers
	WHERE question_id = {question_id}""")
    return get_data_from_sql(commend)

def add_answer(question_id, answer):
    id = generate_new_id('answers')
    timestamp = support_functions.get_timestamp()
    commend = (f"""INSERT into answers values({id}, '{timestamp}', 0, {question_id}, 
                '{answer['message']}', NULL, '{answer['username']}');""")
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
    increase_reputation(data[0]['username'], 5)

def vote_down_question(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE questions
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {question_id}""")
    if data[0]['vote_number'] != 0:
        insert_data_to_sql(commend2)
        decrease_reputation(data[0]['username'], 2)

def vote_up_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE answers
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {answer_id}""")
    insert_data_to_sql(commend2)
    increase_reputation(data[0]['username'], 10)
    return data[0]['question_id']

def vote_down_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE answers
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {answer_id}""")
    if data[0]['vote_number'] != 0:
        insert_data_to_sql(commend2)
        decrease_reputation(data[0]['username'], 2)
    return data[0]['question_id']

def raise_views(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 =(f"""UPDATE questions
    SET view_number = {data[0]['view_number'] + 1}
    WHERE id = {question_id}""")
    insert_data_to_sql(commend2)

def get_question_comments(question_id):
    command = (f"""SELECT id, submision_time, message, edited_numbers, username from comments
    WHERE  question_id = {question_id} and answer_id = 0""")
    return get_data_from_sql(command)

def create_comment_for_question(question_id, comment):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command = (f"INSERT into comments values({id}, {question_id}, 0, '{comment['message']}', '{timestamp}', 0, '{comment['username']}');")
    insert_data_to_sql(command)

def get_answer(answer_id):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command = (f"SELECT * from answers WHERE id = {answer_id}")
    return get_data_from_sql(command)

def get_answer_comments(answer_id):
    command = (f"""SELECT id, submision_time, message, edited_numbers, username from comments
    WHERE  answer_id = {answer_id}""")
    return get_data_from_sql(command)

def create_comment_for_answer(answer_id, comment):
    id = generate_new_id('comments')
    timestamp = support_functions.get_timestamp()
    command1 = (f"""SELECT * from answers
    WHERE id = {answer_id}""")
    data = get_data_from_sql(command1)
    command2 = (f"""INSERT into comments values({id}, {data[0]['question_id']}, {answer_id},
                    '{comment['message']}', '{timestamp}', 0, '{comment['username']}');""")
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

def search_in_questions(search):
    command = (f"""SELECT * from questions
        WHERE title LIKE '%{search}%'
        OR message LIKE '%{search}%'""")
    return get_data_from_sql(command)

def get_sorted_questions(order_by, order_direction):
    commend = (f"""SELECT * from questions
        ORDER BY {order_by} {order_direction}""")
    return get_data_from_sql(commend)

#TODO dodanie strony lub innego sposobu komunikowania o dublującym się użytkowniku
def register(registration_data):
    if check_for_existing_user(registration_data['username']):
        print('Użytkownik istnieje')
        return
    timestamp = support_functions.get_timestamp()
    password = support_functions.secure_password(registration_data['password'])
    command = (f"INSERT into users values( '{registration_data['username']}', '{password}', '{timestamp}', 0);")
    insert_data_to_sql(command)

def check_for_existing_user(username):
    commend = ("SELECT username from users")
    all_users = get_data_from_sql(commend)
    for i in all_users:
        if i['username'] == username:
            return True
    else:
        return False
    
def check_password(username):
    command = (f"""SELECT * from users
        WHERE username LIKE '{username}'""")
    password = get_data_from_sql(command)
    return password[0]['password']

def get_users():
    command = ("""SELECT 
    users.username, 
    users.registration_date, 
    users.reputation,
    COALESCE(questions.questions_table, 0) AS number_of_questions,
    COALESCE(answers.answers_table, 0) AS number_of_answers,
    COALESCE(comments.comments_table, 0) AS number_of_comments
FROM users
LEFT JOIN (
    SELECT 
        username, 
        COUNT(*) AS questions_table
    FROM questions
    GROUP BY username
) questions ON users.username = questions.username
LEFT JOIN (
    SELECT 
        username, 
        COUNT(*) AS answers_table
    FROM answers
    GROUP BY username
) answers ON users.username = answers.username
LEFT JOIN (
    SELECT 
        username, 
        COUNT(*) AS comments_table
    FROM comments
    GROUP BY username
) comments ON users.username = comments.username;""")
    return get_data_from_sql(command)

def get_specific_user_data(username):
    command = (f"""SELECT 
    users.username, 
    users.registration_date, 
    users.reputation,
    COALESCE(questions.questions_table, 0) AS number_of_questions,
    COALESCE(answers.answers_table, 0) AS number_of_answers,
    COALESCE(comments.comments_table, 0) AS number_of_comments
FROM users
LEFT JOIN (
    SELECT 
        username, 
        COUNT(*) AS questions_table
    FROM questions
    GROUP BY username
) questions ON users.username = questions.username
LEFT JOIN (
    SELECT 
        username, 
        COUNT(*) AS answers_table
    FROM answers
    GROUP BY username
) answers ON users.username = answers.username
LEFT JOIN (
    SELECT 
        username, 
        COUNT(*) AS comments_table
    FROM comments
    GROUP BY username
) comments ON users.username = comments.username
WHERE users.username = '{username}';""")
    return get_data_from_sql(command)

def get_user_questions(username):
    commend = (f"""SELECT * from questions 
                WHERE username = '{username}'
               ORDER BY submision_time DESC""")
    return get_data_from_sql(commend)

def get_user_answers(username):
    commend = (f"""SELECT * from answers
                WHERE username = '{username}'
               ORDER BY submision_time DESC""")
    return get_data_from_sql(commend)

def get_user_comments(username):
    commend = (f"""SELECT * from comments 
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
    increase_reputation(answer_data[0]['username'], 15)
    return answer_data[0]['question_id']

def unaccept_answer(answer_id):
    command2 = (f"SELECT * from answers WHERE id = {answer_id}")
    answer_data = get_data_from_sql(command2)
    command = (f"""UPDATE answers
    SET accept_status = NULL
    WHERE id = {answer_id};""")
    insert_data_to_sql(command)
    decrease_reputation(answer_data[0]['username'], 15)
    return answer_data[0]['question_id']

def increase_reputation(username, reputation):
    commend1 = (f"SELECT * from users WHERE username = '{username}';")
    data = get_data_from_sql(commend1)
    commend2 =(f"""UPDATE users
    SET reputation = {data[0]['reputation'] + reputation}
    WHERE username = '{username}'""")
    insert_data_to_sql(commend2)

def decrease_reputation(username, reputation):
    commend1 = (f"SELECT * from users WHERE username = '{username}';")
    data = get_data_from_sql(commend1)
    commend2 =(f"""UPDATE users
    SET reputation = {data[0]['reputation'] - reputation}
    WHERE username = '{username}'""")
    insert_data_to_sql(commend2)

def list_of_tags():
    commend = (f"""SELECT tags.id, tags.name, COUNT(question_tags.tag_id) AS used_times  from tags
                LEFT JOIN question_tags ON tags.id = question_tags.tag_id
                GROUP BY tags.id
                ORDER BY tags.id""")
    return get_data_from_sql(commend)