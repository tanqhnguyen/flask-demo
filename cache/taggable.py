from models.redis_connection import get_client

def _tags_redis_key(instance):
    return ':'.join([instance.__tablename__, 'tags', str(instance.id)])

def delete_tags(instance):
    key = _tags_redis_key(instance)
    redis_client = get_client(key)
    redis_client.delete(key)

def get_tags(instance):
    key = _tags_redis_key(instance)
    redis_client = get_client(key)

    if not redis_client.exists(key):
        tags = [tag.json_data()['name'] for tag in instance.tags]
        redis_client.sadd(key, *tags)
        tags = [{"name": tag} for tag in tags]
    else:
        tags = redis_client.smembers(key)
        tags = [{"name": tag} for tag in tags]
    return tags