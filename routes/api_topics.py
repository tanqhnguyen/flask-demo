from flask import Blueprint, url_for, jsonify, request, g
from flask.ext.babel import gettext as _
from decorators import login_required, check_permission, get_topic
from utils import json_error, json_data, json_error_invalid_request, json_error_database, process_order_input

from models import Comment, Topic, db_session, ModelException

from forms import TopicForm, CommentForm

import logging
import cache

api_topics = Blueprint('api_topics', __name__)

# routes
@api_topics.route('/topics/list', methods=["GET"])
def list():
    user = g.user

    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    order = request.args.get('order', '-date_created')

    topics = cache.get_topics(user=user, sort_by=order, limit=limit, offset=offset)
    
    pagination = {
        "total": Topic.count(),
        "offset": int(offset),
        "limit": int(limit)
    }

    return jsonify(dict(data=topics, pagination=pagination))

@api_topics.route('/topics/read', methods=["GET"])
def read():
    pass

@api_topics.route('/topics/create', methods=["POST"])
@login_required(json=True)
def create():
    data = request.get_json()
    
    form = TopicForm(**data)
    if form.validate():
        form_data = form.data
        form_data['ip'] = request.remote_addr

        try:
            topic = g.user.create_topic(**form_data)
            alert = dict(
                type='success',
                messages=_("Your topic has been created successfully. You will be redirected to it shortly")
            )

            redirect = topic.get_url('view')
            cache.update_sorted_topics(topic, 'date_created')
            return jsonify({"data": topic.json_data(), "alert": alert, "redirect": redirect})
        except ModelException, me:
            db_session.rollback()
            return json_error(type=me.type, messages=me.message)
        except Exception, e:
            logging.error(e)
            db_session.rollback()
            return json_error_database()

    else:
        return json_error(type="VALIDATION_FAILED", messages=form.errors)

@api_topics.route('/topics/vote', methods=["POST"])
@login_required(json=True)
@get_topic(json=True)
def vote():
    topic = g.topic
    data = request.get_json()
    up = data.get('up', True)

    try:
        vote = topic.vote(user=g.user, ip=request.remote_addr, up=up)
        if vote.id:
            # this is an updated vote
            if vote.changed:
                points = topic.update_points(up=up, points=2)
                topic.user.update_points(up=up, points=6)
            else:
                points = topic.points
        else:
            # this is a new vote
            points = topic.update_points(up)
            user_points = 1
            if up:
                user_points = 5
            topic.user.update_points(up=up, points=user_points)
        
        db_session.commit()
        data = {
            "points": points
        }

        cache.update_topic(topic.id, topic)
        cache.update_sorted_topics(topic, 'points')
        return jsonify({"data": data})
    except Exception, e:
        logging.error(e)
        db_session.rollback()
        return json_error_database()

@api_topics.route('/topics/unvote', methods=["POST"])
@login_required(json=True)
@get_topic(json=True)
def unvote():
    topic = g.topic
    vote = topic.unvote(g.user)

    if vote:
        try:
            topic.update_points(up= not vote.up)

            user_points = 1
            if vote.up:
                user_points = 5
            topic.user.update_points(up= not vote.up, points=user_points)

            db_session.commit()
            data = {
                "points": topic.points
            }

            cache.update_topic(topic.id, topic)
            cache.update_sorted_topics(topic, 'points')
            return jsonify({"data": data})
        except Exception, e:
            logging.error(e)
            return json_error_database()
    else:
        return json_error_invalid_request()

@api_topics.route('/topics/search', methods=["GET"])
def search():
    query = request.args.get('query')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    result = Topic.search(query, offset=offset, limit=limit)
    topics = result.get('data')

    pagination = dict(
        limit=limit,
        offset=offset,
        total=Topic.count_search(query)
    )

    return jsonify(dict(
        data=[topic.json_data() for topic in topics],
        pagination=pagination
    ))

"""
Comments
"""
@api_topics.route('/topics/comments/create', methods=["POST"])
@login_required(json=True)
@get_topic(json=True)
def comment_create():
    data = request.get_json()
    topic = g.topic
    
    form = CommentForm(**data)
    if form.validate():
        form_data = form.data
        form_data['user'] = g.user
        form_data['ip'] = request.remote_addr

        try:
            comment = topic.create_comment(**form_data)
            topic.update_comment_count()
            topic.update_user_comment_count(user_id=comment.user_id)

            db_session.commit()

            cache.update_topic(topic.id, topic)
            cache.update_sorted_topics(topic, 'comment_count')
            return jsonify({"data": comment.json_data()})
        except ModelException, me:
            db_session.rollback()
            return json_error(type=me.type, messages=me.message)
        except Exception, e:
            logging.error(e)
            db_session.rollback()
            return json_error_database()
    else:
        return json_error(type="VALIDATION_FAILED", messages=form.errors)

@api_topics.route('/topics/comments/list', methods=["GET"])
@get_topic(json=True)
def comment_list():
    topic = g.topic
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)

    data = topic.get_comments(limit=limit, offset=offset, json=True)
    pagination = {
        'limit': int(limit),
        'offset': int(offset),
        'total': topic.comment_count
    }

    return jsonify({"data": data, 'pagination': pagination})

@api_topics.route('/topics/comments/delete', methods=["POST"])
@login_required(json=True)
@check_permission('delete_comment')
def comment_delete():
    data = request.get_json()

    id = data.get('id')

    comment = Comment.find_by_pk(id)

    if comment:
        try:
            comment.topic.update_comment_count(offset=-1)
            comment.topic.update_user_comment_count(offset=-1, user_id=comment.user_id)
            comment.delete()
            db_session.commit()

            cache.update_topic(comment.topic.id, comment.topic)
            cache.update_sorted_topics(comment.topic, 'comment_count')
            return json_data(data)
        except Exception:
            db_session.rollback()
            return json_error_database()
    else:
        return json_error_invalid_request()