from app import app
from flask import render_template, request
from .spell_check import *

@app.route('/', methods=['GET', 'POST'])
def index():
    TextToCheck = ''

    if request.method == "POST":
        TextToCheck = request.form.get("TextToCheck")
        TextToCheck_List = parse_txt(TextToCheck)
        results = check_word(TextToCheck_List)
        print("Input Text")
        print(TextToCheck+"\n")
        print("Incorrectly Spelled Words")
        results_words = []
        for idx in results:
            print(TextToCheck_List[idx])
            results_words.append(TextToCheck_List[idx])

        return render_template("index.html", misspelled_words=results_words)

    return render_template("index.html")

@app.route('/about')
def about():
    return "About"