from flask import Blueprint, url_for, jsonify, request, g
from flask.ext.babel import gettext as _
from decorators import login_required, check_permission, get_question
from utils import json_error, json_error_invalid_request, json_error_database, hash, now_ms

from models import Article, Vote, Comment, db_session

from forms import QuestionForm, AnswerForm

import logging

api_questions = Blueprint('api_questions', __name__)

# routes
@api_questions.route('/questions/list', methods=["GET"])
def list():
    pass

@api_questions.route('/questions/read', methods=["GET"])
def read():
    pass

@api_questions.route('/questions/create', methods=["POST"])
@login_required(json=True)
def create():
    data = request.get_json()
    
    form = QuestionForm(**data)
    if form.validate():
        form_data = form.data
        form_data['ip'] = request.remote_addr
        question = g.user.create_question(**form_data)
        
        return jsonify({"data": question.json_data()})
    else:
        return json_error(type="VALIDATION_FAILED", messages=form.errors)

"""
Comments
"""
@api_questions.route('/questions/comments/create', methods=["POST"])
@login_required(json=True)
@get_question(json=True)
def comment_create():
    pass

"""
Answers
"""
@api_questions.route('/questions/answers/create', methods=["POST"])
@login_required(json=True)
@get_question(json=True)
def answer_create():
    user = g.user
    question = g.question
    ip = request.remote_addr
    content = request.get_json().get('content')

    form = AnswerForm(content=content)
    if form.validate():
        form_data = form.data
        form_data['ip'] = ip
        form_data['user'] = user
        try:
            answer = question.create_answer(**form_data)
            question.update_answer_count()
            db_session.commit()
            return jsonify({"data": answer.json_data()})
        except Exception, e:
            logging.error(e)
            db_session.rollback()
            return json_error_database()
    else:
        return json_error(type="VALIDATION_FAILED", messages=form.errors)

@api_questions.route('/questions/answers/list', methods=["GET"])
@get_question(json=True)
def answer_list():
    question = g.question
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)

    answers = question.get_answers(limit=limit, offset=offset, json=True)
    pagination = dict(
        limit=int(limit),
        offset=int(offset),
        total=question.answer_count
    )
    return jsonify(dict(data=answers, pagination=pagination))