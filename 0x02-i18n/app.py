#!/usr/bin/env python3
"""
Basic Babel setup
"""
from flask import Flask, render_template, request, g, session
from flask_babel import Babel, gettext
import pytz
import datetime

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
    languages = app.config['LANGUAGES']
    local = request.args.get("locale")
    if local in languages:
        return local

    if g.user:
        local = g.user.get('locale')
        if local in languages:
            return local

    preferred_local = request.headers.get('Accept-Language')

    if preferred_local:
        for entry in preferred_local.split(',')[1:]:
            lang = entry.split(';')[0]
            if lang in languages:
                return lang

    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Infer appropriate time zone """

    """Find timezone parameter in URL parameters"""
    tzp = request.args.get('timezone')
    if tzp:
        try:
            pytz.timezone(tzp)
            return tzp
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    """Find time zone from user settings"""
    if g.user:
        tzp = g.user.get('timezone')
        if tzp:
            try:
                pytz.timezone(tzp)
                return tzp
            except pytz.exceptions.UnknownTimeZoneError:
                pass
    """Default to UTC"""
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def main():
    """
    simply outputs Welcome to Holberton
    """
    fr_format = "%d %b %Y à %H:%M:%S"
    en_format = '%b %d, %Y, %I:%M:%S %p'
    format = fr_format if get_locale() != 'en' else en_format
    utc_time = datetime.utcnow()
    timezone = pytz.timezone(get_timezone())
    localized_time = utc_time.astimezone(timezone)

    formatted_time = localized_time.strftime(format)
    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(debug=True)
