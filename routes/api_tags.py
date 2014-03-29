from flask import Blueprint, jsonify, request
from utils import json_error

from models import Tag, Article, Topic

api_tags = Blueprint('api_tags', __name__)

@api_tags.route('/tags/autocomplete', methods=["GET"])
def autocomplete():
    query = request.args.get('query')

    return jsonify({'data': Tag.autocomplete(query)})

@api_tags.route('/tags/list', methods=["GET"])
def list():
    name = request.args.get('name')
    type = request.args.get('type', 'articles')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    data = []
    
    pagination = dict(
        limit=limit,
        offset=offset,
        total=0
    )
    if type == 'articles':
        data = Article.list_by_tag(name=name, limit=limit, offset=offset, json=True)
        pagination['total'] = Article.count_by_tag(name=name)
    elif type == 'topics':
        data = Topic.list_by_tag(name=name, limit=limit, offset=offset, json=True)
        pagination['total'] = Topic.count_by_tag(name=name)

    return jsonify(dict(
        data=data,
        pagination=pagination
    ))

