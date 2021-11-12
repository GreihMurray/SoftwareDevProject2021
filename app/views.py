"""
Routing file that holds the information for the separate webpage links.
/index: main page for the spellchecker
"""
from app import app
from flask import render_template, request
from .spell_check import *

# Handles the about page with basic information about how to use the spell checker
@app.route('/')
@app.route('/about')
def about_page():
    return render_template("about.html")

# Handles the index page, which contains the spellchecking system 
@app.route('/index', methods=['GET', 'POST'])
def index_page():
    if request.method == "POST":
        langSelect = request.form.get("LangSelect")
        print("Selected Language: ", langSelect)
        TextToCheck = request.form.get("TextToCheck")
        input_list, word_list = parse_txt(TextToCheck)
        results = check_word(input_list, word_list)
        print("Input Text")
        print(TextToCheck+"\n")
        print("Incorrectly Spelled Words")
        results_words = []
        recommendations = []
        for idx in results:
            print(input_list[idx])
            word = input_list[idx]
            recommendations.append((word, word_candidates(word)))
            print(recommendations)
        for idx in results:
            print(input_list[idx])
        for i in range (0, len(input_list)):
            if i in results:
                results_words.append(('Misspelled_words', input_list[i]))
            else:
                results_words.append(('', input_list[i]))

        return render_template("index.html", misspelled_words=results_words, recommendations=recommendations, langSelect=langSelect)

    return render_template("index.html")

@app.route('/about')
def about():
    return "About"
