from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import (questions_data, sql_manager, data_const, support_functions, answers_data,
comments_data, tags_data, user_data, votes_data)

app = Flask(__name__)

app.secret_key = b'1234567890'

#TODO
#poprawić url for w templatkach xD

@app.route('/')
def main_page():
    questions = questions_data.get_latest()
    return render_template('main_page.html', questions = questions, headers = data_const.QUESTIONS_HEADERS)

@app.route('/list')
def list_questions():
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction')
    if (order_by or order_direction) == None:
        questions = questions_data.get_questions()
    else:
        questions = questions_data.get_sorted_questions(order_by, order_direction)
    return render_template('list.html', questions = questions, headers = data_const.QUESTIONS_HEADERS)

@app.route('/add_question', methods = ["POST", "GET"])
def add_question():
    if request.method == "POST":
        question = request.form
        id = questions_data.add_question(question)
        return redirect(url_for('question', id = id))
    else:
        return render_template('add_question.html')
    
@app.route('/question/<id>')
def question(id):
    sql_manager.raise_views(id)
    question = questions_data.get_question(id)
    answers = answers_data.get_answers_for_question(id)
    comments = comments_data.get_question_comments(id)
    tags = tags_data.get_qustion_tags(id)
    return render_template('question.html', question = question, question_headers = data_const.QUESTIONS_HEADERS,
    answers = answers, answer_headers = data_const.ANSWER_HEADERS, comments = comments, comment_headers = data_const.COMMENT_HEADERS,
    tags = tags)

@app.route('/question/<question_id>/new_answer', methods = ["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        answer = request.form
        answers_data.add_answer(question_id, answer)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('add_answer.html', question_id = question_id)

@app.route('/question/<question_id>/delete')
def question_delete(question_id):
    questions_data.delete_question(question_id)
    return redirect(url_for('list_questions'))

@app.route('/question/<question_id>/edit', methods = ["POST", "GET"])
def question_edit(question_id):
    question = questions_data.get_question(question_id)
    if request.method == "POST":
        answer = request.form
        questions_data.edit_question(question_id, answer)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('edit_question.html', question = question)
    
@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    data = answers_data.delete_answer(answer_id)
    return redirect(url_for('question', id = data[0]['question_id']))

@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    votes_data.vote_up_question(question_id)
    return redirect(url_for('question', id = question_id))


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    votes_data.vote_down_question(question_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    question_id = votes_data.vote_up_answer(answer_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    question_id = votes_data.vote_down_answer(answer_id)
    return redirect(url_for('question', id = question_id))

@app.route('/question/<question_id>/new_question_comment', methods = ["POST", "GET"])
def new_question_comment(question_id):
    if request.method == "POST":
        comment = request.form
        comments_data.create_comment_for_question(question_id, comment)
        return redirect(url_for('question', id = question_id))
    else:
        return render_template('add_comment_for_question.html', question_id = question_id)
    
@app.route('/answer/<answer_id>')
def answer(answer_id):
    answer = answers_data.get_answer(answer_id)
    comments = comments_data.get_answer_comments(answer_id)
    return render_template('answer.html', answer = answer, answer_headers = data_const.ANSWER_HEADERS,
    comments = comments ,comment_headers = data_const.COMMENT_HEADERS)

@app.route('/answer/<answer_id>/new_answer_comment', methods = ["POST", "GET"])
def new_answer_comment(answer_id):
    if request.method == "POST":
        comment = request.form
        comments_data.create_comment_for_answer(answer_id, comment)
        return redirect(url_for('answer', answer_id = answer_id))
    else:
        return render_template('add_comment_for_answer.html', answer_id = answer_id)

@app.route('/answer/<answer_id>/edit', methods = ["POST", "GET"])
def edit_answer(answer_id):
    answer = answers_data.get_answer(answer_id)
    if request.method == "POST":
        edited_data = request.form
        answers_data.edit_answer(answer_id, edited_data)
        return redirect(url_for('answer', answer_id = answer_id))
    else:
        return render_template('edit_answer.html', answer = answer)

@app.route('/question_comment/<comment_id>/edit', methods = ["POST", "GET"])
def edit_question_comment(comment_id):
    comment = comments_data.get_comment(comment_id)
    if request.method == "POST":
        edited_data = request.form
        comments_data.edit_comment(comment_id, edited_data)
        return redirect(url_for('question', id = comment[0]['question_id']))
    else:
        return render_template('edit_question_comment.html', comment_id = comment_id, comment = comment)
    
@app.route('/answer_comment/<comment_id>/edit', methods = ["POST", "GET"])
def edit_answer_comment(comment_id):
    comment = comments_data.get_comment(comment_id)
    if request.method == "POST":
        edited_data = request.form
        comments_data.edit_comment(comment_id, edited_data)
        return redirect(url_for('answer', answer_id = comment[0]['answer_id']))
    else:
        return render_template('edit_answer_comment.html', comment_id = comment_id, comment = comment)
    
@app.route('/question_comment/<comment_id>/delete')
def delete_question_comment(comment_id):
    question_id = comments_data.delete_question_comment(comment_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer_comment/<comment_id>/delete')
def delete_answer_comment(comment_id):
    answer_id = comments_data.delete_question_comment(comment_id)
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
    tags_data.delete_question_tag(question_id, tag_id)
    return redirect(url_for('question', id = question_id))

@app.route('/search')
def search():
    search = request.args.get('search')
    results = questions_data.search_in_questions(search)
    return render_template('search.html', search = search, results = results, headers = data_const.QUESTIONS_HEADERS)

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        user_data.register(request.form)
        return redirect(url_for('main_page'))
    else:
        return render_template('register.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        if support_functions.login(request.form):
            session['username'] = request.form['username']
            return redirect(url_for('main_page'))
        else:
            return redirect(url_for('main_page'))
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))

@app.route('/users')
def users():
    users = user_data.get_users()
    return render_template('users.html', users = users, headers = data_const.USERS_HEADERS)
    
@app.route('/user/<username>')
def user_page(username):
    data = user_data.get_specific_user_data(username)
    questions, answers, comments = support_functions.get_user_entries(username)
    print(comments)
    return render_template('user_page.html', username = username, data = data, question_headers = data_const.QUESTIONS_HEADERS,
    answer_headers = data_const.ANSWER_HEADERS, comment_headers = data_const.COMMENT_HEADERS, questions = questions, answers = answers,
    comments = comments)

@app.route('/answer/<answer_id>/accept')
def accept_answer(answer_id):
    question_id = answers_data.accept_answer(answer_id)
    return redirect(url_for('question', id = question_id))

@app.route('/answer/<answer_id>/unaccept')
def unaccept_answer(answer_id):
    question_id = answers_data.unaccept_answer(answer_id)
    return redirect(url_for('question', id = question_id))

@app.route('/tags')
def tags():
    tags = tags_data.list_of_tags()
    return render_template('tags.html', headers = data_const.TAGS_LIST_HEADERS, tags = tags) 

@app.route('/bonus-questions')
def bonus_questions():
    return 'bonus questions'


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
