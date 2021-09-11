from app import app
from flask import render_template

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        req = request.form
        print(req)
        return redirect(request.url)

    return render_template("index.html")

@app.route('/about')
def about():
    return "About"