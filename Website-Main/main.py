#from crypt import methods
import json
from flask import Flask, render_template, request
from flask_session import Session
from flask import jsonify 

import sqlalchemy.engine
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__, template_folder="templates")
app.debug = True

# secret key
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///safety_program.db"
app.config['SESSION_TYPE'] = "filesystem"

import database

### Init db
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/safety_programs", methods=['GET', 'POST'])
def p_db():
    if request.method == 'GET':
        sp_names = {
            "Names": database.parse_db()
        }
        return jsonify(sp_names)

    if request.method == 'POST':
        print(request.get_json())
        return 'Success', 200

if __name__ == "__main__":
    app.run()
           