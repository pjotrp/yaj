from yaj import app
from flask import render_template

@app.route("/test")
def test_page():
    return "Yet another journal! Well, early days!"

@app.route("/")
def main_page():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template("index.html",title="YAJ",user=user)
