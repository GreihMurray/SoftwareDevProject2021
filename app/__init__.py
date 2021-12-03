"""
Init file for run.py
Imports Flask framework and imports views.py (for different webpages)
"""
from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PLOIKJUHTN049382048FFNGI3GOCNVK3U'
from app import views
