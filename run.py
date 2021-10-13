"""
Main run file for the website.
After activating the virtual environment in your terminal of choice,
activate with >>python run.py
"""
from app import app

if __name__ == '__main__':
    app.run(debug=True)
