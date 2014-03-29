from models.database import db_session

from utils import get_remote_side_class, get_remote_side

from models.redis_connection import get_client

class Taggable():
    def _tags_redis_key(self):
        return ':'.join([self.__tablename__, 'tags', str(self.id)])

    def create_tags(self, tags, commit=False):
        if not tags:
            return self

        tags = [tag.lower() for tag in tags]
        tags = set(tags)

        # delete old tags
        for tag in self.tags:
            db_session.delete(tag)

        cls = get_remote_side_class(self, 'tags')
        ref_name = get_remote_side(self, 'tags')
        # create new tags
        for t in tags:
            tag = cls()
            tag.name = t
            setattr(tag, ref_name, self.id)
            db_session.add(tag)

        key = self._tags_redis_key()
        redis_client = get_client(key)
        redis_client.delete(key)

        if commit:
            db_session.commit()
        return self

    """
    Gets the tags from redis. If there is no tag stored in redis, fetch it from postgres
    """
    def get_tags(self):
        key = self._tags_redis_key()
        redis_client = get_client(key)

        if not redis_client.exists(key):
            tags = [tag.json_data()['name'] for tag in self.tags]
            redis_client.sadd(key, *tags)
            tags = [{"name": tag} for tag in tags]
        else:
            tags = redis_client.smembers(key)
            tags = [{"name": tag} for tag in tags]
        return tags

    @classmethod
    def list_by_tag(cls, name, limit=10, offset=0, json=False):
        obj = cls() # due to the lazy-init of backref, we can't have tags before creating new instance
        ref_name = get_remote_side(obj, 'tags')
        Tag = get_remote_side_class(obj, 'tags')
        tags = Tag.query.filter(getattr(Tag, ref_name) != None, Tag.name == name).order_by(ref_name+' DESC').limit(limit).offset(offset).all()

        ref_name = ref_name.split("_")[0]
        records = [getattr(tag, ref_name) for tag in tags]

        if json:
            return [record.json_data() for record in records]

        return records

    @classmethod
    def count_by_tag(cls, name):
        obj = cls() # due to the lazy-init of backref, we can't have tags before creating new instance
        ref_name = get_remote_side(obj, 'tags')
        Tag = get_remote_side_class(obj, 'tags')
        return Tag.query.filter(getattr(Tag, ref_name) != None, Tag.name == name).count()