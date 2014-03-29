from functools import wraps
from flask import g, redirect, url_for, request, abort
from utils import json_error_unauthorized_access, json_error_invalid_request
from models import Article, Question, Topic


def login_required(next='/', json=False):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                if json:
                    return json_error_unauthorized_access()
                else:
                    return redirect(url_for('site.page', name='login', next=next))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def check_permission(name, next='/', orCheck=None, andCheck=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                return redirect(url_for('site.page', name='login', next=next))
            else:
                has_permission = g.user.has_permission(name)
                approve = has_permission
                if orCheck is not None:
                    approve = approve or orCheck()
                if andCheck is not None:
                    approve = approve and andCheck()
                if not approve:
                    return json_error_unauthorized_access()
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def get_article(json=False):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            # support both json and normal request
            if not data:
                data = request.args
                # now kiss
                data = dict(request.args.items() + kwargs.items())

            article_id = data.get('id')
            article_id = data.get('article_id', article_id)

            article = Article.find_by_pk(article_id)
            if not article:
                if json:
                    return json_error_invalid_request()
                else:
                    return abort(400)

            g.article = article
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def get_question(json=False):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            # support both json and normal request
            if not data:
                data = request.args
                # now kiss
                data = dict(request.args.items() + kwargs.items())

            question_id = data.get('id')
            question_id = data.get('question_id', question_id)

            question = Question.find_by_pk(question_id)
            if not question:
                if json:
                    return json_error_invalid_request()
                else:
                    return abort(400)

            g.question = question
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def get_topic(json=False):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            # support both json and normal request
            if not data:
                data = request.args
                # now kiss
                data = dict(request.args.items() + kwargs.items())

            topic_id = data.get('id')
            topic_id = data.get('topic_id', topic_id)

            topic = Topic.find_by_pk(topic_id)
            if not topic:
                if json:
                    return json_error_invalid_request()
                else:
                    return abort(400)

            g.topic = topic
            return f(*args, **kwargs)
        return decorated_function
    return wrapper