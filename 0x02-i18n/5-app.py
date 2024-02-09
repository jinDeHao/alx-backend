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


def get_user(id) -> dict:
    """
    Mock logging in
    """
    return users[int(id)] if id is not None else None


@app.before_request
def before_request():
    """
    Mock logging in
    """
    id = request.args.get('login_as', None)
    g.user = get_user(id)


@babel.localeselector
def get_locale() -> str:
    """
    Get locale from request
    """
    lang = request.args.get('locale')
    if lang and lang in app.config['LANGUAGES']:
        return lang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def main() -> str:
    """
    simply outputs Welcome to Holberton
    """
    return render_template('5-index.html', user=g.user)


if __name__ == '__main__':
    app.run(debug=True)
