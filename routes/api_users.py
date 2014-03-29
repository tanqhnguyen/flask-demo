from flask import Blueprint, jsonify, request, redirect

from decorators import login_required, check_permission, get_article
from utils import json_error, json_data, json_error_invalid_request, json_error_database, process_order_input

from models import User

api_users = Blueprint('api_users', __name__)

@api_users.route('/users/avatar', methods=["GET"])
def avatar():
    id = request.args.get('id')
    size = request.args.get('size', 100)

    user = User.find_by_pk(id)

    if not user:
        return json_error_invalid_request()

    avatar = None
    if user.login_type == 'facebook':
        avatar = "http://graph.facebook.com/%s/picture?width=%s&height=%s" % (user.login_id, size, size)
    elif user.login_type == 'github':
        avatar = "http://www.gravatar.com/avatar/%s?s=%s" % (user.social_data.get('gravatar_id'), size)
    elif user.login_type == 'google':
        avatar = user.social_data.get('picture') + "?sz=" + size
    
    if not avatar:
        return json_error_invalid_request()
    return redirect(avatar, 302);

@api_users.route('/users/ban', methods=["POST"])
@login_required(json=True)
@check_permission('ban_user')
def ban():
    data = request.get_json()
    id = data.get('id')
    reason = data.get('reason', 'You have been banned')

    user = User.find_by_pk(id)

    if user:
        user.ban(reason=reason, commit=True)
        return json_data(data)
    else:
        return json_error_invalid_request()

@api_users.route('/users/unban', methods=["POST"])
@login_required(json=True)
@check_permission('unban_user')
def unban():
    data = request.get_json()
    id = data.get('id')

    user = User.find_by_pk(id)

    if user:
        user.unban(commit=True)
        return json_data(data)
    else:
        return json_error_invalid_request()
