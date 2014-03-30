from flask import Blueprint, render_template, url_for, g, request, session, redirect
from decorators import login_required, check_permission

from models import Article, Question, Topic
import cache

site = Blueprint('site', __name__, template_folder="templates")

@site.route('/')
@site.route('/articles.html')
def articles():
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

@site.route('/questions.html')
def questions():
    context = {
        'js_module': 'questions',
        'style': 'questions'
    }

    user = g.user

    questions = Question.list_for_user(limit=10, offset=0, user=user)

    context['questions'] = questions
    return render_template('site/questions.html', **context)

@site.route('/topics.html')
def topics():
    context = {
        'js_module': 'topics',
        'style': 'topics'
    }

    user = g.user

    topics = cache.get_topics(user=user, sort_by='-date_created')
    latest_articles = []
    

    context['topics'] = topics
    context['latest_articles'] = latest_articles

    return render_template('site/topics.html', **context)

@site.route('/login.html')
def login():
    return render_template('site/login.html')

@site.route('/search')
def search():
    query = request.args.get('query', '')
    query = query.strip()

    if len(query) == 0:
        return redirect('/')

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    # search articles
    result = Article.search(query, offset=offset, limit=limit)
    articles = result.get('data')
    articles = [article.json_data() for article in articles]

    context = {
        'search': query,
        'offset': offset,
        'limit': limit,
        'js_module': 'search',
        'style': 'search',
        'articles': articles,
        'total_article': result['raw']['total_found'],
        'total_topic': Topic.count_search(query)
    }
    return render_template('site/search.html', **context)

@site.route('/approve-article')
@login_required(next='/approve-article')
@check_permission(name='approve_article', next='/approve-article')
def approve_article():
    context = {
        'js_module': 'approve_article',
        'style': 'approve_article'
    }
    return render_template('site/approve_article.html', **context)

@site.route('/tags/<name>.html')
def tags(name):
    name = name.lower()

    articles = Article.list_by_tag(name=name, json=True)

    context = {}
    context['articles'] = articles
    context['total_article'] = Article.count_by_tag(name=name)
    context['total_topic'] = Topic.count_by_tag(name=name)
    context['tag'] = name
    context['style'] = 'tags'
    context['js_module'] = 'tags'
    return render_template('site/tags.html', **context)

@site.route('/logout.html')
def logout():
    del session['user_id']
    return redirect(url_for('site.page', name='articles'))

@site.route('/<name>.html')
def page(name):
    name = '_'.join(name.split('-'))
    return render_template('site/'+name+'.html')