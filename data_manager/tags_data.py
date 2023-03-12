from data_manager.sql_manager import get_data_from_sql, insert_data_to_sql
from data_manager import support_functions, sql_manager

def get_tags():
    command = ("SELECT * from tags")
    return get_data_from_sql(command)

def add_tag_to_question(tag_id, question_id):
    command = (f"INSERT into question_tags values({question_id}, {tag_id})")
    insert_data_to_sql(command)

def create_new_tag(new_tag):
    new_id = sql_manager.generate_new_id('tags')
    new_tag = sql_manager.clear_inputs(new_tag)
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

def list_of_tags():
    commend = (f"""SELECT tags.id, tags.name, COUNT(question_tags.tag_id) AS used_times  from tags
                LEFT JOIN question_tags ON tags.id = question_tags.tag_id
                GROUP BY tags.id
                ORDER BY tags.id""")
    return get_data_from_sql(commend)