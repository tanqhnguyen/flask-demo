from models.redis_connection import get_client

def _comment_count_redis_key(instance, user_id):
    return ':'.join([instance.__tablename__, str(instance.id), 'user_comment_count', str(user_id)])

def update_user_comment_count(instance, user_id, offset=1):
    key = _comment_count_redis_key(instance, user_id)
    redis_client = get_client(key)
    if offset > 0:
        result = redis_client.incr(key, offset)
    else:
        result = redis_client.decr(key, abs(offset))
    return int(result)

def get_user_comment_count(instance, user_id):
    key = _comment_count_redis_key(instance, user_id)
    redis_client = get_client(key)
    count = redis_client.get(key)
    if not count:
        return None

    return int(count)