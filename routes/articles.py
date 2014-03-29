from flask import Blueprint, render_template, url_for, g, request
from decorators import login_required, check_permission, get_article

from models import Article
from flask.ext.babel import gettext as _

articles = Blueprint('articles', __name__, template_folder="templates")

@articles.route('/submit-article.html')
@login_required(next='/submit-article.html')
def submit():
    context = {
        'js_module': 'submit_article',
        'style': 'submit_article',
        'sub_title': _('Submit article'),
        'title': _('Submit article')
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
    article.check_vote(user)
    article.check_comment(user)

    article.update_view_count(ip=request.remote_addr, user=user, commit=True)

    article_data = article.json_data()
    article_data['comments'] = article.get_comments(json=True)
    context = {
        'js_module': 'view_article',
        'style': 'view_article',
        'article': article_data,
        'title': article.title,
        'sub_title': article.title
    }
    return render_template('article/view.html', **context)