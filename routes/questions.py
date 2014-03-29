from flask import Blueprint, render_template, url_for, g
from decorators import login_required, check_permission, get_question

questions = Blueprint('questions', __name__, template_folder="templates")

@questions.route('/ask-question.html')
@login_required(next='/ask-question.html')
def submit():
    context = {
        'js_module': 'ask_question',
        'style': 'ask_question'
    }
    return render_template('question/ask.html', **context)

@questions.route('/q/<slug>-<int:id>.html')
@get_question()
def view(slug, id):
    question = g.question
    user = g.user
    question.check_vote(user)
    question.check_comment(user)
    question.check_answer(user)

    question_data = question.json_data()
    question_data['answers'] = question.get_answers(json=True)
    
    context = {
        'js_module': 'view_question',
        'style': 'view_question',
        'question': question_data,
        'title': question.title
    }
    return render_template('question/view.html', **context)