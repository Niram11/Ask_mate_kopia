from datetime import datetime
from data_manager import sql_manager

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M")
    return str(timestamp)

def add_tag(tag, question_id):
    tags = sql_manager.get_tags()
    for i in tags:
        if i['name'] == tag:
            sql_manager.add_tag_to_question(i['id'], question_id)
            return
    new_tag_id = sql_manager.create_new_tag(tag)
    sql_manager.add_tag_to_question(new_tag_id, question_id)