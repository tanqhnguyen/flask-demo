from flask import Blueprint, render_template, g, request
from decorators import login_required, get_topic

topics = Blueprint('topics', __name__, template_folder="templates")

from models import Topic

import cache.topic as cache

@topics.route('/topics.html')
def render_topics():
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

@topics.route('/create-topic.html')
@login_required(next='/create-topic.html')
def create():
    context = {
        'js_module': 'create_topic',
        'style': 'create_topic'
    }
    return render_template('topics/create.html', **context)

@topics.route('/t/<slug>-<int:id>.html')
@get_topic()
def view(slug, id):
    topic = g.topic
    user = g.user

    if topic.update_view_count(ip=request.remote_addr, user=user, commit=True):
        cache.update_topic(topic.id, topic)
        cache.update_sorted_topics(topic, 'view_count')

    topic_data = topic.json_data()
    topic_data['comments'] = topic.get_comments(json=True)
    topic_data['user_vote'] = Topic.check_vote(user, topic.id)
    topic_data['user_comment'] = Topic.check_comment(user, topic.id)
    context = {
        'js_module': 'view_topic',
        'style': 'view_topic',
        'topic': topic_data,
        'sub_title': topic.title
    }
    return render_template('topics/view.html', **context)