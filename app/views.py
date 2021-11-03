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
    lang_dictionaries = {}
    lang_dictionaries["Irish"] = load_dict('cumulative_irish.csv')
    if request.method == "POST":
        all_data = request.get_data(as_text=True)
        print('All data: ', all_data)
        langSelect = request.form.get("LangSelect")
        print("Selected Language: ", langSelect)
        TextToCheck = request.form.get("TextToCheck")
        results = []
        if langSelect == "English":
            TextToCheck_List = parse_txt(TextToCheck)
            results = check_word(TextToCheck_List)
        else:
            TextToCheck_List = parse_txt_other_lang(TextToCheck)
            results = check_other_lang(TextToCheck_List, lang_dictionaries[langSelect])
        print("Input Text")
        print(TextToCheck+"\n")
        print("Incorrectly Spelled Words")
        results_words = []
        recommendations = []
        for idx in results:
            print(TextToCheck_List[idx])
            word = TextToCheck_List[idx]
            if langSelect == 'English':
                recommendations.append((word, word_candidates(word)))
            else:
                print("Add other lang recommendations")
                recommendations.append((word, ''))
            print(recommendations)
        for idx in results:
            print(TextToCheck_List[idx])
        for i in range (0, len(TextToCheck_List)):
            if i in results:
                results_words.append(('Misspelled_words', TextToCheck_List[i]))
            else:
                results_words.append(('', TextToCheck_List[i]))

        return render_template("index.html", misspelled_words=results_words, recommendations=recommendations, langSelect=langSelect)

    return render_template("index.html")

@app.route('/about')
def about():
    return "About"
