"""
Routing file that holds the information for the separate webpage links.
/index: main page for the spellchecker
"""

from app import app
from flask import render_template, request, session, jsonify
from .spell_check import *
from .context import *
from flask_babel import Babel

app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

@babel.localeselector
def get_locale():
    try:
        lang = session['language']
    except KeyError:
        print('KEY')
        lang = 'en'

    return lang

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
    lang_dictionaries["Irish"] = loadDictionary('IrishCorpus/filtered_db_output.json')
    lang_dictionaries["English"] = loadDictionary('EnglishCorpus/Filtered_English_Dict.json')
    if request.method == "POST":
        all_data = request.get_data(as_text=True)
        langSelect = request.form.get("LangSelect")
        print("Selected Language: ", langSelect)
        TextToCheck = request.form.get("TextToCheck")

        input_list, word_list, results_words, recommendations = logicCntrl(TextToCheck, langSelect, lang_dictionaries)

        return render_template("index.html", misspelled_words=results_words, recommendations=recommendations, langSelect=langSelect)

    return render_template("index.html")

@app.route('/process_lang', methods=['GET', 'POST'])
def process_lang():
    if request.method == "POST":
        page_lang = request.get_json()
        session['language'] = page_lang[0]['language']
        print(page_lang)
        print(session['language'])

    results = {'processed': 'true'}
    return jsonify(results)

