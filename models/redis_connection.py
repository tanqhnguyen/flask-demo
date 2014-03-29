import redis
import config

from hash_ring import HashRing

redis_servers = []
for redis_config in config.REDIS:
    redis_servers.append(":".join([redis_config["host"], str(redis_config["port"])]))

ring = HashRing(redis_servers)

def get_redis_config(string):
    string = string.split(":")
    host = string[0]
    port = string[1]
    for redis_config in config.REDIS:
        if redis_config["host"] == host and str(redis_config["port"]) == str(port):
            return redis_config

    return None

cache = {}

def get_client(key):
    config_string = ring.get_node(key)

    client = cache.get(config_string)
    if client is None:
        config = get_redis_config(config_string)
        client = redis.StrictRedis(host=config["host"], port=config["port"], password=config["password"], db=0)
        cache[config_string] = client

    return client