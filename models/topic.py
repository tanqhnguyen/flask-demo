from flask import url_for

from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.babel import gettext as _
from slugify import slugify

from .database import Base, db_session

from .sphinx import get_sphinx_client

from utils import now_ms, escape

from .mixins.votable import Votable
from .mixins.commentable import Commentable
from .mixins.recordable import Recordable
from .mixins.taggable import Taggable
from .mixins.pointable import Pointable
from .mixins.searchable import Searchable
from .mixins.loggable import Loggable
from .tag import Tag

class Topic(Base, Votable, Commentable, Recordable, Taggable, Pointable, Searchable, Loggable):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    date_created = Column(BigInteger, default=now_ms)
    content = Column(Text)
    ip = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('topics', order_by=date_created, cascade='all,delete'))

    def json_data(self):
        return {
            "content": escape(self.content),
            "title": self.title,
            "id": self.id,
            "date_created": self.date_created,
            "user": self.user.json_data(),
            "tags": self.get_tags(),
            "points": self.points,
            "comment_count": self.comment_count,
            "urls": self.get_url(),
            "user_vote": self.user_vote,
            "user_comment": self.user_comment,
            "view_count": self.view_count
        }

    def get_url(self, name=None):
        urls = {
            'view': url_for('topics.view', slug=slugify(self.title), id=self.id)
        }

        if name:
            return urls.get(name)

        return urls

    @classmethod
    def cache_key(cls, id):
        return ":".join([cls.__tablename__, str(id)])

    @classmethod
    def list(cls, **kwargs):
        json = kwargs.get('json', False)
        order_by = kwargs.get('order', 'date_created DESC')
        topics = cls.query.order_by(order_by).limit(kwargs.get('limit', 10)).offset(kwargs.get('offset', 0)).all()

        if json:
            return [topic.json_data() for topic in topics]
        return topics

    @classmethod
    def count(cls):
        return cls.query.count()

    """
    A convenient method for listing topics and do filtering based on the current user
    """
    @classmethod
    def list_for_user(cls, **kwargs):
        user = kwargs.get('user')
        topics = cls.list(**kwargs)
        if user:
            topics = [user.check_topic(topic).json_data() for topic in topics]
        else:
            topics = [topic.json_data() for topic in topics]

        return topics