from flask import Flask, render_template, request
from wtforms.widgets.core import TextArea
from flask_wtf import FlaskForm
from wtforms import StringField, form

app = Flask(__name__, template_folder="templates")
app.debug = True

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
           