from flask import url_for

from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.babel import gettext as _
from slugify import slugify

from .database import Base

from .sphinx import get_sphinx_client

from sqlalchemy import orm

from utils import now_ms, hash, escape

from .mixins.votable import Votable
from .mixins.commentable import Commentable
from .mixins.pointable import Pointable

class Answer(Base, Votable, Commentable, Pointable):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    date_created = Column(BigInteger, default=now_ms)
    content = Column(Text)
    ip = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('answers', order_by=date_created, cascade='all,delete'))
    question = relationship('Question', backref=backref('answers', order_by=date_created, cascade='all,delete'))

    def json_data(self):
        return dict(
            id = self.id,
            content = escape(self.content),
            date_created = self.date_created,
            user = self.user.json_data()
        )