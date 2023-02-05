"""
This layer contains logic related to Flask, such as server, 
routes, request handling, session, and so on. 
This is the only file to be imported from Flask.
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
