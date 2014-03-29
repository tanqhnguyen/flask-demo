from flask import Blueprint, current_app, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import config
from models import User
from flask.ext.babel import gettext as _
import json


social_auth = Blueprint('social_auth', __name__)

oauth = OAuth(current_app)

# Facebook
# facebook = oauth.remote_app(
#     'facebook',
#     consumer_key=config.FACEBOOK['key'],
#     consumer_secret=config.FACEBOOK['secret'],
#     request_token_params={'scope': ['publish_stream', 'email', 'read_friendlists']},
#     base_url='https://graph.facebook.com',
#     request_token_url=None,
#     access_token_url='/oauth/access_token',
#     authorize_url='https://www.facebook.com/dialog/oauth'
# )

# @social_auth.route('/callback/facebook')
# @facebook.authorized_handler
# def callback_facebook(res):
#     if res is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['access_token'] = (res['access_token'], '')

#     me = facebook.get('/me')
#     data = {
#         'login_id': me.data['id'],
#         'login_type': 'facebook',
#         'social_data': me.data,
#         'email': me.data['email'],
#         'access_token': res['access_token'],
#         'name': me.data.get('name', me.data.get('username')),
#         'avatar': "http://graph.facebook.com/%s/picture" % me.data['id']
#     }
#     user = User.create_or_update(**data)
#     session['user_id'] = user.id
#     next = request.args.get('next', url_for('site.home'))
#     return redirect(next)

# @social_auth.route('/auth/facebook')
# def auth_facebook():
#     return facebook.authorize(callback=url_for('social_auth.callback_facebook',
#         next=request.args.get('next') or None,
#         _external=True))

# @facebook.tokengetter
# def get_facebook_oauth_token():
#     return session.get('access_token')

# Github
github = oauth.remote_app(
    'github',
    consumer_key=config.GITHUB['key'],
    consumer_secret=config.GITHUB['secret'],
    request_token_params={'scope': 'user:email,public_repo,user:follow'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@social_auth.route('/auth/github')
def auth_github():
    return github.authorize(callback=url_for('social_auth.callback_github', 
        next=request.args.get('next') or None,
        _external=True))

@social_auth.route('/callback/github')
@github.authorized_handler
def callback_github(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['access_token'] = (resp['access_token'], '')
    me = github.get('user')
    data = {
        'login_id': me.data['id'],
        'login_type': 'github',
        'social_data': me.data,
        'email': me.data['email'],
        'access_token': resp['access_token'],
        'name': me.data.get('name', me.data.get('login')),
        'avatar': "http://www.gravatar.com/avatar/%s" % me.data['gravatar_id']
    }
    user = User.create_or_update(**data)
    session['user_id'] = user.id
    next = request.args.get('next', url_for('site.home'))
    return redirect(next)


@github.tokengetter
def get_github_oauth_token():
    return session.get('access_token')
            
# Google
google = oauth.remote_app(
    'google',
    consumer_key=config.GOOGLE['key'],
    consumer_secret=config.GOOGLE['secret'],
    request_token_params={
        'scope': ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/plus.me','https://www.googleapis.com/auth/plus.login']
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@social_auth.route('/auth/google')
def auth_google():
    next = request.args.get('next', None)
    return google.authorize(callback=url_for('social_auth.callback_google', _external=True), state=next)

@social_auth.route('/callback/google')
@google.authorized_handler
def callback_google(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['access_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    data = {
        'login_id': me.data['id'],
        'login_type': 'google',
        'social_data': me.data,
        'email': me.data['email'],
        'access_token': resp['access_token'],
        'name': me.data.get('name', me.data['email'].split("@")[0]),
        'avatar': "https://plus.google.com/s2/photos/profile/%s" % me.data['id']
    }
    user = User.create_or_update(**data)

    session['user_id'] = user.id
    next = request.args.get('state', url_for('site.home'))
    return redirect(next)

@google.tokengetter
def get_google_oauth_token():
    return session.get('access_token')