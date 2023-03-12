from data_manager.sql_manager import get_data_from_sql, insert_data_to_sql
from data_manager import support_functions, sql_manager


def register(registration_data):
    if check_for_existing_user(registration_data['username']):
        print('Użytkownik istnieje')
        return
    username = sql_manager.clear_inputs(registration_data['username'])
    timestamp = support_functions.get_timestamp()
    password = support_functions.secure_password(registration_data['password'])
    command = (f"INSERT into users values( '{username}', '{password}', '{timestamp}', 0);")
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