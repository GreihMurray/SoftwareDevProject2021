from app import app
from flask import render_template, request

@app.route('/', methods=['GET', 'POST'])
def index():
    TextToCheck = ''

    if request.method == "POST":
        TextToCheck = request.form.get("TextToCheck")
        print(TextToCheck)

    return render_template("index.html", TestData=TextToCheck)

@app.route('/about')
def about():
    return "About"