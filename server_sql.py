from flask import Flask, render_template, request, redirect, url_for
from data_manager import sql_manager, data_const, support_functions

app = Flask(__name__)

@app.route('/')
def main_page():
    questions = sql_manager.get_latest()
    return render_template('main_page.html', questions = questions, headers = data_const.QUESTIONS_HEADERS)

@app.route('/list')
def list_questions():
    questions = sql_manager.get_questions()
    return render_template('list.html', questions = questions, headers = data_const.QUESTIONS_HEADERS)

@app.route('/add_question', methods = ["POST", "GET"])
def add_question():
    if request.method == "POST":
        question = request.form
        id = sql_manager.add_question(question)
        return redirect(url_for('question', id = id))
    else:
        return render_template('add_question.html')
    
@app.route('/question/<id>')
def question(id):
    sql_manager.raise_views(id)
    question = sql_manager.get_question(id)
    answers = sql_manager.get_answers_for_question(id)
    comments = sql_manager.get_question_comments(id)
    tags = sql_manager.get_qustion_tags(id)
    return render_template('question.html', question = question, question_headers = data_const.QUESTIONS_HEADERS,
    answers = answers, answer_headers = data_const.ANSWER_HEADERS, comments = comments, comment_headers = data_const.COMMENT_HEADERS,
    tags = tags)

@app.route('/question/<question_id>/new_answer', methods = ["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        answer = request.form
        sql_manager.add_answer(question_id, answer)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('add_answer.html', question_id = question_id)

@app.route('/question/<question_id>/delete')
def question_delete(question_id):
    sql_manager.delete_question(question_id)
    return redirect(url_for('list_questions'))

@app.route('/question/<question_id>/edit', methods = ["POST", "GET"])
def question_edit(question_id):
    question = sql_manager.get_question(question_id)
    if request.method == "POST":
        answer = request.form
        sql_manager.edit_question(question_id, answer)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('edit_question.html', question = question)
    
@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    data = sql_manager.delete_answer(answer_id)
    return redirect(url_for('question', id = data[0]['question_id']))

@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    sql_manager.vote_up_question(question_id)
    return redirect(url_for('question', id = question_id))


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    sql_manager.vote_down_question(question_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    question_id = sql_manager.vote_up_answer(answer_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    question_id = sql_manager.vote_down_answer(answer_id)
    return redirect(url_for('question', id = question_id))

@app.route('/question/<question_id>/new_question_comment', methods = ["POST", "GET"])
def new_question_comment(question_id):
    if request.method == "POST":
        comment = request.form
        sql_manager.create_comment_for_question(question_id, comment)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('add_comment_for_question.html', question_id = question_id)
    
@app.route('/answer/<answer_id>')
def answer(answer_id):
    answer = sql_manager.get_answer(answer_id)
    comments = sql_manager.get_answer_comments(answer_id)
    return render_template('answer.html', answer = answer, answer_headers = data_const.ANSWER_HEADERS,
    comments = comments ,comment_headers = data_const.COMMENT_HEADERS)

@app.route('/answer/<answer_id>/new_answer_comment', methods = ["POST", "GET"])
def new_answer_comment(answer_id):
    if request.method == "POST":
        comment = request.form
        sql_manager.create_comment_for_answer(answer_id, comment)
        return redirect(url_for('answer', answer_id = answer_id))
    else:
        return render_template('add_comment_for_answer.html', answer_id = answer_id)

@app.route('/answer/<answer_id>/edit', methods = ["POST", "GET"])
def edit_answer(answer_id):
    answer = sql_manager.get_answer(answer_id)
    if request.method == "POST":
        edited_data = request.form
        sql_manager.edit_answer(answer_id, edited_data)
        return redirect(url_for('answer', answer_id = answer_id))
    else:
        return render_template('edit_answer.html', answer = answer)

@app.route('/question_comment/<comment_id>/edit', methods = ["POST", "GET"])
def edit_question_comment(comment_id):
    comment = sql_manager.get_comment(comment_id)
    if request.method == "POST":
        edited_data = request.form
        sql_manager.edit_comment(comment_id, edited_data)
        return redirect(url_for('question', id = comment[0]['question_id']))
    else:
        return render_template('edit_question_comment.html', comment_id = comment_id, comment = comment)
    
@app.route('/answer_comment/<comment_id>/edit', methods = ["POST", "GET"])
def edit_answer_comment(comment_id):
    comment = sql_manager.get_comment(comment_id)
    if request.method == "POST":
        edited_data = request.form
        sql_manager.edit_comment(comment_id, edited_data)
        return redirect(url_for('answer', answer_id = comment[0]['answer_id']))
    else:
        return render_template('edit_answer_comment.html', comment_id = comment_id, comment = comment)
    
@app.route('/question_comment/<comment_id>/delete')
def delete_question_comment(comment_id):
    question_id = sql_manager.delete_question_comment(comment_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer_comment/<comment_id>/delete')
def delete_answer_comment(comment_id):
    answer_id = sql_manager.delete_question_comment(comment_id)
    return redirect(url_for('answer', answer_id = answer_id))

@app.route('/question/<question_id>/add_tag', methods = ["POST", "GET"])
def add_tag(question_id):
    if request.method == "POST":
        new_tag = request.form
        support_functions.add_tag(new_tag['tag'], question_id)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('add_tag.html', question_id = question_id)

@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    sql_manager.delete_question_tag(question_id, tag_id)
    return redirect(url_for('question', id = question_id))

if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
