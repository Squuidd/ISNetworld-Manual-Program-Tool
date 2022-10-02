from enum import unique
from unicodedata import name
import sqlalchemy.engine
from flask_sqlalchemy import SQLAlchemy

from main import app
import safety_program_creator as spc

import os

db = SQLAlchemy(app)

class Safety_Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    path = db.Column(db.String(), unique=True, nullable=False)

db.create_all()
db.session.commit()

# create function that gets all the file names and paths and updates the db all at once

def update_db():
    path = "Safety Programs"
    dir_list = os.listdir(path)

    for file in dir_list:
        if file[-4:] == "docx":
            sp = Safety_Program(name=file[:-5], path=spc.findPath(file))
            db.session.add(sp)
    
    db.session.commit

update_db()

programs = db.session.query(Safety_Program)
print(programs.all())
