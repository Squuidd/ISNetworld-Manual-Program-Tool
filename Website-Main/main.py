from flask import Flask, render_template, request
from flask_session import Session


import os

app = Flask(__name__, template_folder="templates")
app.debug = True

# secret key
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SESSION_TYPE'] = "filesystem"

import database as db

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
           