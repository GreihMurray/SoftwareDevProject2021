"""
Init file for run.py
Imports Flask framework and imports views.py (for different webpages)
"""
from flask import Flask
app = Flask(__name__)
from app import views
