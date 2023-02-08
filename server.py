"""
This layer contains logic related to Flask, such as server, 
routes, request handling, session, and so on. 
This is the only file to be imported from Flask.
"""
from flask import Flask, render_template, request, redirect
from data_manager import data, data_const

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/list')
def list_questions():
    a = data.read_csv()
    matrix = data.sort_matrix_by_column_with_headers(a, column = 2)
    return render_template('list.html', questions = matrix)

@app.route('/add_question')
def add_question():
    return render_template('add_question.html')

@app.route('/add_question_task', methods = ["POST"])
def add_question_task():
    question = request.form
    data.add_new_question(question)
    return redirect('list')

app.route('/question/<question_id>')
def question(question_id):
    return 'question' + str(question_id)

app.route('/add-question')
def add_question():
    return 'add_question'

app.route('/question/<question_id>/delete')
def question_delete(question_id):
    return 'question_delete' + str(question_id)

app.route('/question/<question_id>/edit')
def question_edit(question_id):
    return 'question_edit' + str(question_id)

app.route('/question/<question_id>/new-answer')
def new_answer(question_id):
    return 'new_answer' + str(question_id)

app.route('/answer/<question_id>/delete')
def answer_delete(question_id):
    return 'answer_delete' + str(question_id)

app.route('/question/<question_id>/vote-up')
def vote_up(question_id):
    return 'vote_up' + str(question_id)

app.route('/question/<question_id>/vote-down')
def vote_down(question_id):
    return 'vote_down' + str(question_id)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
