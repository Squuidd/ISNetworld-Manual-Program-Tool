#from crypt import methods
import json

from flask import Flask, render_template, request, send_file
from flask_session import Session
from flask import jsonify 

import sqlalchemy.engine
from flask_sqlalchemy import SQLAlchemy

import safety_program_creator as spc

import os

app = Flask(__name__, template_folder="templates")
app.debug = True

# secret key
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///safety_program.db"
app.config['SESSION_TYPE'] = "filesystem"

db = SQLAlchemy(app)
db.init_app(app)
class Safety_Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    path = db.Column(db.String(), unique=False, nullable=False)

# create function that gets all the file names and paths and updates the db all at once

def update_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    path = "Safety Programs"
    dir_list = os.listdir(path)

    for file in dir_list:
        if file[-4:] == "docx":
            sp = Safety_Program(name=file[:-5], path=spc.findPath(file))
            db.session.add(sp)

    db.session.commit()
    db.session.close_all()

# Only returns list of program names
def parse_db():
    programs = db.session.query(Safety_Program)
    docs = []
    print(programs)
    for program in programs:
        program_data = []
        program_data.append(program.name)
        program_data.append(program.id)
        docs.append(program_data)
        # print(program.name)
    return docs

# update_db()
with app.app_context():
    db.create_all()
    db.session.commit()
session = db.session



def convert_to_path(programs : list):
    output = []
    for program in programs:
        program += '.docx'
        path = spc.findPath(program)
        output.append(path)
    return output

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/safety_programs", methods=['GET', 'POST'])
def p_db():
    if request.method == 'GET':
        sp_names = {
            "Programs": parse_db()
        }
        return jsonify(sp_names)

    if request.method == 'POST':
        json_data = request.get_json()
        
        program_list = json_data["programs"]
        is_manual = json_data["manual"]
        company_name = json_data["company_name"]

        if is_manual:
            blob = spc.create_manual(
                file=spc.findPath("safety_manual.docx"),
                safety_documents= convert_to_path(programs=program_list),
                company_name=company_name
            )
        else:
            blob = spc.create_program(
                files=convert_to_path(programs=program_list),
                company_name=company_name
            )
        
        return blob, 200


if __name__ == "__main__":
    app.run()
           