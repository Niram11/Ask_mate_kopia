import psycopg2
from psycopg2.extras import RealDictCursor
from data_manager import support_functions

def get_questions():
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("SELECT * from questions")
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
    id = generate_new_id_for_question()
    timestamp = support_functions.get_timestamp()
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"INSERT into questions values({id}, '{timestamp}', 0, 0, '{question['title']}', '{question['message']}', NULL);")
    return id

def generate_new_id_for_question():
    conn = psycopg2.connect(database = 'postgres', user = 'postgres', password = 'postgres')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("SELECT MAX(id) from questions")
    data = cursor.fetchall()
    return int(data[0]['max']) + 1

