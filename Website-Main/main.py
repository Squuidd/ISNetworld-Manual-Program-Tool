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

import database

# Init db
db = SQLAlchemy(app)



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
            "Programs": database.parse_db()
        }
        return jsonify(sp_names)

    if request.method == 'POST':
        json_data = request.get_json()
        program_list = json_data["programs"]

        is_manual = json_data["manual"]
        
        print(convert_to_path(programs=program_list), is_manual)

        if is_manual:
            spc.create_manual(  
                file=spc.findPath("safety_manual.docx"),
                safety_documents= convert_to_path(programs=program_list),
                company_name="Test Name 1 LLC."
            )
        else:
            spc.create_program(
                files=convert_to_path(programs=program_list),
                company_name="Test Name 1 LLC."
            )
            print("program")
        
        return 'Success', 200

@app.route("/download_sm")
def download_sm():
    path = "Output/new_safety_manual.docx"
    return send_file(path, as_attachment=True)

@app.route("/download_sp")
def download_sp():
    # return zip
    pass




if __name__ == "__main__":
    app.run()
           