"""
Routing file that holds the information for the separate webpage links.
/index: main page for the spellchecker
"""

from app import app
from flask import render_template, request, session, jsonify
from .spell_check import *
from .context import *
from .error_model import *

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
    # Load Dictionaries
    lang_dictionaries = {}
    lang_dictionaries["Irish"] = loadDictionary('IrishCorpus/filtered_db_output.json')
    lang_dictionaries["English"] = loadDictionary('EnglishCorpus/Filtered_English_Dict.json')
    # Load Error Models
    lang_error_models = {}
    lang_error_models["Irish"] = loadEM('IrishCorpus/letter_pairs_small.json')
    lang_error_models["English"] = loadEM('EnglishCorpus/letter_pairs_en.json')
    # Build Tries
    lang_word_trie = {}
    lang_word_trie["Irish"] = load_word_list(lang_dictionaries["Irish"].keys())
    lang_word_trie["English"] = load_word_list(lang_dictionaries["English"].keys())
    if request.method == "POST":
        all_data = request.get_data(as_text=True)
        langSelect = request.form.get("LangSelect")
        print("Selected Language: ", langSelect)
        TextToCheck = request.form.get("TextToCheck")

        input_list, word_list = parse_txt(TextToCheck)

        result_words = []
        recommendations = []
        for wordIdx, token in enumerate(input_list):
            if wordIdx in word_list:
                if wordIdx != 0:
                    prevW = toLower(input_list[wordIdx - 1])
                else:
                    prevW = ""
                if wordIdx != len(input_list) - 1:
                    aftW = toLower(input_list[wordIdx + 1])
                else:
                    aftW = ""
                recs, context_err = logicCntrl(input_list[wordIdx], [prevW, aftW], langSelect, lang_dictionaries[langSelect],
                              lang_error_models[langSelect], lang_word_trie[langSelect])

                if input_list[wordIdx] == recs[0]:
                    result_words.append(('', input_list[wordIdx]))
                elif context_err:
                    result_words.append(('Recommendation_words', input_list[wordIdx]))
                    recommendations.append([input_list[wordIdx], recs])
                else:
                    result_words.append(('Misspelled_words', input_list[wordIdx]))
                    recommendations.append([input_list[wordIdx], recs[:5]])
            else:
                result_words.append(('', input_list[wordIdx][:5]))
        print(recommendations)

        # input_list, word_list, results_words, recommendations = logicCntrl(TextToCheck, langSelect, lang_dictionaries)

        return render_template("index.html", misspelled_words=result_words, recommendations=recommendations, langSelect=langSelect)

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

