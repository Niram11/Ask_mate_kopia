"""
This layer contains logic related to Flask, such as server, 
routes, request handling, session, and so on. 
This is the only file to be imported from Flask.
"""
from flask import Flask, render_template, request, redirect, url_for
from data_manager import data, data_const, data_functions

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/list', methods=["POST", "GET"])
def list_questions():
    matrix = data_functions.sort_matrix_by_column_with_headers(data_functions.read_csv(data_const.QUESTIONS),
                                                               data_const.VIEW_NUMBER_POSITION)
    return render_template('list.html', questions=matrix)


@app.route('/add_question', methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        question = request.form
        a = data.add_new_question(question, data_const.QUESTIONS)
        return redirect(url_for('question', id=a))
    else:
        return render_template('add_question.html')


@app.route('/question/<id>')
def question(id):
    data = data_functions.read_csv(data_const.QUESTIONS)
    question_id = data_functions.get_data_with_id_and_headers(data, id)
    answers = data_functions.read_csv(data_const.ANSWERS)
    answers_with_id = data_functions.get_data_with_id_and_headers(answers, id)
    return render_template('question.html', data=question_id, answers=answers_with_id)


@app.route('/question/<question_id>/delete')
def question_delete(question_id):
    all = data_functions.read_csv(data_const.QUESTIONS)
    data.delete_question_with_id(all, question_id)
    return redirect(url_for('list_questions'))


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def question_edit(question_id):
    data = data_functions.read_csv(data_const.QUESTIONS)
    question = data_functions.get_question_with_id(data, question_id)
    if request.method == "POST":
        data_functions.edit_data_with_id(data, question_id, request.form)
        return redirect(url_for('question', id=question_id))
    else:
        return render_template('edit_question.html', question=question)


@app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return 'new_answer' + str(question_id)


@app.route('/answer/<question_id>/delete')
def answer_delete(question_id):
    return 'answer_delete' + str(question_id)


@app.route('/question/<question_id>/vote-up')
def vote_up(question_id):
    return 'vote_up' + str(question_id)


@app.route('/question/<question_id>/vote-down')
def vote_down(question_id):
    return 'vote_down' + str(question_id)


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
