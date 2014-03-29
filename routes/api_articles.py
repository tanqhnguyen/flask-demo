from flask import Blueprint, url_for, jsonify, request, g
from flask.ext.babel import gettext as _
from decorators import login_required, check_permission, get_article
from utils import json_error, json_data, json_error_invalid_request, json_error_database, process_order_input

from models import Article, Comment, db_session, ModelException

from forms import ArticleForm, CommentForm

import logging

api_articles = Blueprint('api_articles', __name__)

# helpers
def is_article_owner():
    article_id = request.args.get('id')
    article_id = request.args.get('article_id', article_id)
    return Article.is_owner(article_id, g.user.id)

# routes
@api_articles.route('/articles/list', methods=["GET"])
def list():
    is_active = request.args.get('is_active', 1);   
    is_active = int(is_active) 
    is_active = is_active == 1

    user = g.user

    if not user:
        is_active = True
    elif user and not user.has_permission('approve_article'):
        is_active = True

    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    order = request.args.get('order', '-date_created')
    order_strings = process_order_input(order)

    articles = Article.list_for_user(is_active=is_active, limit=limit, offset=offset, user=user, order=order_strings)
    
    pagination = {
        "total": Article.count(),
        "offset": int(offset),
        "limit": int(limit)
    }

    return jsonify(dict(data=articles, pagination=pagination))

@api_articles.route('/articles/read', methods=["GET"])
def read():
    pass

@api_articles.route('/articles/create', methods=["POST"])
@login_required(json=True)
def create():
    data = request.get_json()
    
    form = ArticleForm(**data)
    if form.validate():
        form_data = form.data
        form_data['ip'] = request.remote_addr
        article = g.user.create_article(**form_data)

        alert = dict(
            type='success',
            messages=_("Your article has been submitted successfully. The staff will approve it soon. Thank you for your contribution")
        )

        redirect = url_for("site.page", name="home")
        
        return jsonify({"data": article.json_data(), "alert": alert, "redirect": redirect})
    else:
        return json_error(type="VALIDATION_FAILED", messages=form.errors)

@api_articles.route('/articles/update', methods=["POST"])
@login_required(json=True)
@check_permission('update_article', orCheck=is_article_owner)
@get_article(json=True)
def update():
    article = g.article
    user = g.user
    data = request.get_json()
    form = ArticleForm(**data)
    if form.validate():
        form_data = form.data
        data = form_data
        data['ip'] = request.remote_addr
        data['user'] = user

        # Make sure that users cant change article status
        try:
            if not user.has_permission('approve_article'):
                del data['is_active']
        except Exception:
            pass

        article.update(**data)
        return jsonify({"data": article.json_data()})
    else:
        return json_error(type="VALIDATION_FAILED", messages=form.errors)

@api_articles.route('/articles/approve', methods=['POST'])
@login_required(json=True)
@check_permission('approve_article')
@get_article(json=True)
def approve():
    article = g.article
    data = {}
    data['ip'] = request.remote_addr
    data['user'] = g.user
    data['is_active'] = True

    article.update(**data)
    # also update the user point
    article.user.update_points(up=True, points=25, commit=True)
    return jsonify({"data": article.json_data()})

@api_articles.route('/articles/delete', methods=["POST"])
@login_required(json=True)
@check_permission('delete_article', orCheck=is_article_owner)
@get_article(json=True)
def delete():
    article = g.article
    article.delete(commit=True)
    return jsonify({"data": article.json_data()})

@api_articles.route('/articles/vote', methods=["POST"])
@login_required(json=True)
@get_article(json=True)
def vote():
    article = g.article
    data = request.get_json()
    up = data.get('up', True)

    try:
        vote = article.vote(user=g.user, ip=request.remote_addr, up=up)
        if vote.id:
            # this is an updated vote
            if vote.changed:
                points = article.update_points(up=up, points=2)
                article.user.update_points(up=up, points=11)
            else:
                points = article.points
        else:
            # this is a new vote
            points = article.update_points(up)
            user_points = 1
            if up:
                user_points = 10
            article.user.update_points(up=up, points=user_points)
        
        db_session.commit()
        data = {
            "points": points
        }
        return jsonify({"data": data})
    except Exception, e:
        logging.error(e)
        db_session.rollback()
        return json_error_database()

@api_articles.route('/articles/unvote', methods=["POST"])
@login_required(json=True)
@get_article(json=True)
def unvote():
    article = g.article
    vote = article.unvote(g.user)

    if vote:
        try:
            article.update_points(up= not vote.up)

            user_points = 1
            if vote.up:
                user_points = 10
            article.user.update_points(up= not vote.up, points=user_points)

            db_session.commit()
            data = {
                "points": article.points
            }
            return jsonify({"data": data})
        except Exception, e:
            logging.error(e)
            return json_error_database()
    else:
        return json_error_invalid_request()

@api_articles.route('/articles/search', methods=["GET"])
def search():
    query = request.args.get('query')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    result = Article.search(query, offset=offset, limit=limit)
    articles = result.get('data')
    for article in articles:
        article.check_vote(g.user)
        article.check_comment(g.user)

    pagination = dict(
        limit=limit,
        offset=offset,
        total=Article.count_search(query)
    )

    return jsonify(dict(
        data=[article.json_data() for article in articles],
        pagination=pagination
    ))

"""
Comments
"""
@api_articles.route('/articles/comments/create', methods=["POST"])
@login_required(json=True)
@get_article(json=True)
def comment_create():
    data = request.get_json()
    article = g.article
    
    form = CommentForm(**data)
    if form.validate():
        form_data = form.data
        form_data['user'] = g.user
        form_data['ip'] = request.remote_addr

        try:
            comment = article.create_comment(**form_data)
            article.update_comment_count()
            article.update_user_comment_count(user_id=comment.user_id)

            db_session.commit()
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

@api_articles.route('/articles/comments/list', methods=["GET"])
@get_article(json=True)
def comment_list():
    article = g.article
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)

    data = article.get_comments(limit=limit, offset=offset, json=True)
    pagination = {
        'limit': int(limit),
        'offset': int(offset),
        'total': article.comment_count
    }

    return jsonify({"data": data, 'pagination': pagination})

@api_articles.route('/articles/comments/delete', methods=["POST"])
@login_required(json=True)
@check_permission('delete_comment')
def comment_delete():
    data = request.get_json()

    id = data.get('id')

    comment = Comment.find_by_pk(id)

    if comment:
        try:
            comment.article.update_comment_count(offset=-1)
            comment.article.update_user_comment_count(offset=-1, user_id=comment.user_id)
            comment.delete()
            db_session.commit()
            return json_data(data)
        except Exception:
            db_session.rollback()
            return json_error_database()
    else:
        return json_error_invalid_request()