"""
Routing file that holds the information for the separate webpage links.
/index: main page for the spellchecker
"""

from app import app
from flask import render_template, request
from .spell_check import *
from .load_dictionaries import *

def _fix_encoding(string):
    return string.encode('iso-8859-1').decode('utf8')

# Handles the about page with basic information about how to use the spell checker
@app.route('/')
@app.route('/about')
def about_page():
    return render_template("about.html")

# Handles the index page, which contains the spellchecking system 
@app.route('/index', methods=['GET', 'POST'])
def index_page():
    irish_dict = load_dict('cumulative_irish.csv')
    if request.method == "POST":
        langSelect = request.form.get("LangSelect")
        print("Selected Language: ", langSelect)
        TextToCheck = request.form.get("TextToCheck")
        input_list, word_list = parse_txt(TextToCheck)
        results = check_word(input_list, word_list)
        TextToCheck_List = parse_txt(TextToCheck)
        if langSelect == "English":
            results = check_word(TextToCheck_List)
        elif langSelect == "Irish":
            results = check_other_lang(TextToCheck_List, irish_dict)
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
