from app import app
from flask import render_template, request

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        TextToCheck = request.form.get("TextToCheck")
        print(TextToCheck)

    return render_template("index.html")

@app.route('/about')
def about():
    return "About"