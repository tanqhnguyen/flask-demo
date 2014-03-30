from flask import Flask, session, g, request, redirect
from flask.ext.babel import Babel

from models.database import db_session
from social_auth import social_auth

from routes.site import site
from routes.articles import articles
from routes.questions import questions
from routes.topics import topics

from routes.api_articles import api_articles
from routes.api_tags import api_tags
from routes.api_users import api_users
from routes.api_questions import api_questions
from routes.api_topics import api_topics

from models import User
from jinja import filters

from werkzeug.contrib.fixers import ProxyFix


import config

app = Flask(__name__)
app.secret_key = config.SECRET
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config.from_object(config)

# Babel Setup
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(config.LANGUAGES.keys())

app.register_blueprint(social_auth)
app.register_blueprint(site)
app.register_blueprint(articles)
app.register_blueprint(questions)
app.register_blueprint(topics)

app.register_blueprint(api_articles, url_prefix="/api")
app.register_blueprint(api_tags, url_prefix="/api")
app.register_blueprint(api_users, url_prefix="/api")
app.register_blueprint(api_questions, url_prefix="/api")
app.register_blueprint(api_topics, url_prefix="/api")

@app.before_request
def before_request():
    if 'user_id' in session:
        user = User.find_by_pk(int(session['user_id']))
        g.user = user
        if user.is_banned:
            return user.ban_reason
    else:
        g.user = None

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Setup Jinja
app.jinja_env.filters['static'] = filters.static
app.jinja_env.filters['to_json'] = filters.to_json
app.jinja_env.filters['construct_title'] = filters.construct_title

@app.context_processor
def setup_env_detect():
    def is_env(env):
        return env == config.ENV

    return {'is_env': is_env}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)