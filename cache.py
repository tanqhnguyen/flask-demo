from models.redis_connection import get_client
from models import Article
import simplejson as json

def _generate_articles_key(sort_by):
    return ":".join([Article.__tablename__, sort_by])

def fetch_articles(sort_by):
    """Fetches all the articles from postgresql and construct a set sorted by :sort_by DESC
    Args:
        sort_by(str): the sort key applied to articles
    Returns:
        None
    """
    articles = Article.query.filter_by(is_active=True).all()
    key = _generate_articles_key(sort_by)
    redis_client = get_client(key)
    data = dict()
    for article in articles:
        data[str(article.id)] = getattr(article, sort_by)
    redis_client.zadd(key, **data)

def get_articles(user, sort_by, offset=0, limit=10):
    """Gets articles from redis or postgresql
    Args:
        user (User): the current user
        sort_by (str): the sort key
        offset (int): offset
        limit (int): limit
    Returns:
        An array of articles (formatted by json_data) sorted by :sort_by and limited by :limit started from :offset
    """
    rev = sort_by[0] == '-'

    if rev:
        sort_by = sort_by[1:]

    key = _generate_articles_key(sort_by)
    redis_client = get_client(key)
    if not redis_client.exists(key):
        fetch_articles(sort_by)

    start = offset
    stop = offset + limit - 1

    if rev:
        article_ids = redis_client.zrevrange(key, start, stop)
    else:
        article_ids = redis_client.zrange(key, start, stop)

    articles = []

    for id in article_ids:
        articles.append(get_article(id))

    return articles

def get_article(id, user=None):
    """Gets a single article (formatted by json_data) from redis or postgresql
    And performs some pre-filters for the current user
    Args:
        id (int): id
        user (User): the current user
    Returns:
        None if the article is not existed or a dict of article data
    """
    id = int(id)
    key = Article.cache_key(id)
    redis_client = get_client(key)

    article = None
    if not redis_client.exists(key):
        article = Article.find_by_pk(id)
        if article:
            data = article.json_data()
            redis_client.set(key, json.dumps(data))
            article = data
    else:
        if redis_client.type(key) == 'hash':
            print redis_client
        article = json.loads(redis_client.get(key))

    article['user_vote'] = Article.check_vote(user, article['id'])

    return article
