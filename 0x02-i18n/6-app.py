#!/usr/bin/env python3
"""
Basic Babel setup
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext


app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    config for your Flask app
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id):
    """
    Mock logging in
    """
    return users["id"] if id is not None else None


@app.before_request
def before_request():
    """
    Mock logging in
    """
    id = request.args.get('login_as', None)
    g.user = get_user(id)


@babel.localeselector
def get_locale():
    """
    Get locale from request
    """
    cLang = app.config['LANGUAGES']
    lang = request.args.get('locale')
    if lang and lang in cLang:
        return lang

    request_locale = request.accept_languages.best_match(cLang)
    if request_locale:
        return request_locale

    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', strict_slashes=False)
def main():
    """
    simply outputs Welcome to Holberton
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(debug=True)
