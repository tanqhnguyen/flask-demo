from flask import Blueprint, render_template, url_for, g, request
from decorators import login_required, check_permission, get_article

from models import Article
from flask.ext.babel import gettext as _

import cache.article as cache

articles = Blueprint('articles', __name__, template_folder="templates")

@articles.route('/')
@articles.route('/articles.html')
def render_articles():
    context = {
        'js_module': 'articles',
        'style': 'articles'
    }

    user = g.user

    articles = cache.get_articles(user=user, sort_by='-date_created')

    # articles = Article.list_for_user(is_active=True, limit=10, offset=0, user=user)
    # latest_topics = Topic.list_for_user(limit=10, offset=0, user=user)
    # 
    latest_topics = []

    context['articles'] = articles
    context['latest_topics'] = latest_topics
    return render_template('site/articles.html', **context)


@articles.route('/submit-article.html')
@login_required(next='/submit-article.html')
def submit():
    context = {
        'js_module': 'submit_article',
        'style': 'submit_article',
        'sub_title': _('Submit article')
    }
    return render_template('article/submit.html', **context)

@articles.route('/featured-articles.html')
def featured():
    context = {
        'js_module': 'home',
        'style': 'home'
    }

    articles = Article.list_for_user(is_active=True, limit=10, offset=0, user=g.user, order="points DESC")

    context['articles'] = articles

    return render_template('article/featured.html', **context)

@articles.route('/a/<slug>-<int:id>.html')
@get_article()
def view(slug, id):
    article = g.article
    user = g.user

    if article.update_view_count(ip=request.remote_addr, user=user, commit=True):
        cache.update_article(article.id, article)
        cache.update_sorted_article(article, 'view_count')

    article_data = article.json_data()
    article_data['comments'] = article.get_comments(json=True)
    article_data['user_vote'] = Article.check_vote(user, article.id)
    article_data['user_comment'] = Article.check_comment(user, article.id)

    context = {
        'js_module': 'view_article',
        'style': 'view_article',
        'article': article_data,
        'sub_title': article.title
    }
    return render_template('article/view.html', **context)