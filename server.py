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


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
