from data_manager.sql_manager import get_data_from_sql, insert_data_to_sql
from data_manager import sql_manager

def vote_up_question(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE questions
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {question_id}""")
    insert_data_to_sql(commend2)
    sql_manager.increase_reputation(data[0]['username'], 5)

def vote_down_question(question_id):
    commend1 = (f"SELECT * from questions WHERE id = {question_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE questions
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {question_id}""")
    if data[0]['vote_number'] != 0:
        insert_data_to_sql(commend2)
        sql_manager.decrease_reputation(data[0]['username'], 2)

def vote_up_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE answers
    SET vote_number = {data[0]['vote_number'] + 1}
    WHERE id = {answer_id}""")
    insert_data_to_sql(commend2)
    sql_manager.increase_reputation(data[0]['username'], 10)
    return data[0]['question_id']

def vote_down_answer(answer_id):
    commend1 = (f"SELECT * from answers WHERE id = {answer_id};")
    data = get_data_from_sql(commend1)
    commend2 = (f"""UPDATE answers
        SET vote_number = {data[0]['vote_number'] - 1}
        WHERE id = {answer_id}""")
    if data[0]['vote_number'] != 0:
        insert_data_to_sql(commend2)
        sql_manager.decrease_reputation(data[0]['username'], 2)
    return data[0]['question_id']