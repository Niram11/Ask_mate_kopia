"""
This layer contains logic related to Flask, such as server, 
routes, request handling, session, and so on. 
This is the only file to be imported from Flask.
"""
from flask import Flask, render_template
from data_manager import data, data_const

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/list')
def list_questions():
    a = data.read_csv(data_const.QUESTIONS)
    matrix = data.sort_matrix_by_column_with_headers(a,column=3 )
    return render_template('list.html', questions = matrix)

@app.route('/add-question')
def add_question():
    return 'add_question'

app.route('/question/')
def question():
    return 'question'

app.route('/add-question')
def add_question():
    return 'add_question'

app.route('/question/delete')
def question_delete():
    return 'question_delete'

app.route('/question/edit')
def question_edit():
    return 'question_edit'

app.route('/question/new-answer')
def new_answer():
    return 'new_answer'

app.route('/answer/delete')
def answer_delete():
    return 'answer_delete'

app.route('/question/vote-up')
def vote_up():
    return 'vote_up'

app.route('/question/vote-down')
def vote_down():
    return 'vote_down'

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
