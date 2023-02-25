from flask import Flask, render_template, request, redirect, url_for
from data_manager import sql_manager, data_const

app = Flask(__name__)



@app.route('/list')
def list_questions():
    questions = sql_manager.get_questions()
    return render_template('list.html', questions = questions, headers = data_const.QUESTIONS_HEADERS)

@app.route('/add_question', methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        question = request.form
        id = sql_manager.add_question(question)
        return redirect(url_for('question', id = id))
    else:
        return render_template('add_question.html')
    
@app.route('/question/<id>')
def question(id):
    question = sql_manager.get_question(id)
    return render_template('question.html', question = question, headers = data_const.QUESTIONS_HEADERS)

if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )