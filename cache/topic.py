from models.redis_connection import get_client
from models import Topic
import simplejson as json

def _generate_topics_key(sort_by):
    return ":".join([Topic.__tablename__, sort_by])

def fetch_topics(sort_by):
    """Fetches all the topics from postgresql and construct a set sorted by :sort_by DESC
    Args:
        sort_by(str): the sort key applied to topics
    Returns:
        None
    """
    topics = Topic.query.all()
    key = _generate_topics_key(sort_by)
    redis_client = get_client(key)
    data = dict()
    for topic in topics:
        data[str(topic.id)] = getattr(topic, sort_by)
    redis_client.zadd(key, **data)

def get_topics(user, sort_by, offset=0, limit=10):
    """Gets topics from redis or postgresql
    Args:
        user (User): the current user
        sort_by (str): the sort key
        offset (int): offset
        limit (int): limit
    Returns:
        An array of topics (formatted by json_data) sorted by :sort_by and limited by :limit started from :offset
    """
    rev = sort_by[0] == '-'

    if rev:
        sort_by = sort_by[1:]

    key = _generate_topics_key(sort_by)
    redis_client = get_client(key)
    if not redis_client.exists(key):
        fetch_topics(sort_by)

    start = offset
    stop = offset + limit - 1

    if rev:
        topic_ids = redis_client.zrevrange(key, start, stop)
    else:
        topic_ids = redis_client.zrange(key, start, stop)

    topics = []

    for id in topic_ids:
        topics.append(get_topic(id))

    return topics

def get_topic(id, user=None):
    """Gets a single topic (formatted by json_data) from redis or postgresql
    And performs some pre-filters for the current user
    Args:
        id (int): id
        user (User): the current user
    Returns:
        None if the topic is not existed or a dict of topic data
    """
    id = int(id)
    key = Topic.cache_key(id)
    redis_client = get_client(key)

    topic = None
    if not redis_client.exists(key):
        topic = Topic.find_by_pk(id)
        if topic:
            data = topic.json_data()
            redis_client.set(key, json.dumps(data))
            topic = data
    else:
        if redis_client.type(key) == 'hash':
            print redis_client
        topic = json.loads(redis_client.get(key))

    topic['user_vote'] = Topic.check_vote(user, topic['id'])

    return topic

def update_topic(id, topic=None):
    """Updates the cache of article :id
    Args:
        id (int): topic id
        topic (Topic): if not provided, a topic will be queried from postgresql
    Returns:
        Topic
    """
    id = int(id)
    if not topic:
        topic = Topic.find_by_pk(id)

    if topic:
        key = Topic.cache_key(id)
        redis_client = get_client(key)
        data = topic.json_data()
        redis_client.set(key, json.dumps(data))

    return topic

def update_sorted_topics(topic, sort_by):
    key = _generate_topics_key(sort_by)
    redis_client = get_client(key)
    data = dict()
    data[str(topic.id)] = getattr(topic, sort_by)
    redis_client.zadd(key, **data)