import psycopg2
import re
from psycopg2.extras import RealDictCursor


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

def generate_new_id(table):
    try:
        commend = (f"SELECT MAX(id) from {table}")
        data = get_data_from_sql(commend)
        return int(data[0]['max']) + 1
    except:
        return 1

def raise_views(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 =(f"""UPDATE questions
    SET view_number = {data[0]['view_number'] + 1}
    WHERE id = {question_id}""")
    insert_data_to_sql(commend2)

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

def clear_inputs(user_input):
    user_input = re.sub(r"[^a-zA-Z0-9 ]+", "", user_input)
    return user_input