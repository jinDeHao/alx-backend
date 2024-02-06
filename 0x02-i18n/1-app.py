#!/usr/bin/env python3
"""
Basic Babel setup
"""
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    LANGUAGES = ["en", "fr"]

babel.default_locale = Config.LANGUAGES[0]
babel.default_timezone = 'UTC'

@app.route('/')
def main():
    """
    simply outputs Welcome to Holberton
    """
    return render_template('1-index.html')
