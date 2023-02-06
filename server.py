"""
This layer contains logic related to Flask, such as server, 
routes, request handling, session, and so on. 
This is the only file to be imported from Flask.
"""
from data_manager import data_crud
from flask import Flask, render_template
import csv
from server_const import QUESTIONS

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/list')
def list_questions():
    with open(QUESTIONS, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    print(data[0])
    return render_template('list.html', questions = data)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
