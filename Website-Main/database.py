
import sqlalchemy.engine
from flask_sqlalchemy import SQLAlchemy

import safety_program_creator as spc

import os

from app import db


class Safety_Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    path = db.Column(db.String(), unique=False, nullable=False)

# with app.app_context():
#     db.create_all()
#     db.session.commit()


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

    for program in programs:
        program_data = []
        program_data.append(program.name)
        program_data.append(program.id)
        docs.append(program_data)
        # print(program.name)
    return docs

#update_db()
db.create_all()
db.session.commit()

# with app.app_context():
#     db.create_all()
#     db.session.commit()
# session = db.session


# programs = db.session.query(Safety_Program)
# # print(programs.all()[0].name)
# for program in programs:
#     print(program.name)
