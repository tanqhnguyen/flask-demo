from flask import Blueprint, render_template, g, request
from decorators import login_required, get_topic

topics = Blueprint('topics', __name__, template_folder="templates")

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
    topic.check_vote(user)
    topic.check_comment(user)

    topic.update_view_count(ip=request.remote_addr, user=user, commit=True)

    topic_data = topic.json_data()
    topic_data['comments'] = topic.get_comments(json=True)
    context = {
        'js_module': 'view_topic',
        'style': 'view_topic',
        'topic': topic_data,
        'title': topic.title,
        'sub_title': topic.title
    }
    return render_template('topics/view.html', **context)