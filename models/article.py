from flask import url_for

from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.babel import gettext as _
from slugify import slugify

from .database import Base, db_session

from utils import now_ms, escape

from .mixins.votable import Votable
from .mixins.commentable import Commentable
from .mixins.recordable import Recordable
from .mixins.taggable import Taggable
from .mixins.pointable import Pointable
from .mixins.searchable import Searchable
from .mixins.loggable import Loggable
from .comment import Comment

class Article(Base, Votable, Commentable, Recordable, Taggable, Pointable, Searchable, Loggable):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    date_created = Column(BigInteger, default=now_ms)
    content = Column(Text)
    is_active = Column(Boolean, default=False)
    ip = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('articles', order_by=date_created, cascade='all,delete'))

    # @orm.reconstructor
    # def init_on_load(self):
    #     self.user_vote = None
    #     self.user_comment = False

    def json_data(self):
        return {
            "content": escape(self.content),
            "title": self.title,
            "id": self.id,
            "date_created": self.date_created,
            "is_active": self.is_active,
            "user": self.user.json_data(),
            "tags": self.get_tags(),
            "points": self.points,
            "comment_count": self.comment_count,
            "view_count": self.view_count,
            "urls": self.get_url(),
            "user_vote": self.user_vote,
            "user_comment": self.user_comment
        }

    def get_url(self, name=None):
        urls = {
            'view': url_for('articles.view', slug=slugify(self.title), id=self.id)
        }

        if name:
            return urls.get(name)

        return urls

    def update(self, **kwargs):
        old_content = self.content
        old_title = self.title
        old_status = self.is_active

        for attribute in ['content', 'title', 'is_active']:
            value = kwargs.get(attribute)
            if value:
                setattr(self, attribute, value)

        new_tags = kwargs.get('tags')

        if new_tags:
            new_tags = set([tag['name'].lower() for tag in new_tags])

        old_tags = set([tag.name for tag in self.tags])

        record_data = dict(
            user = kwargs.get('user'),
            ip = kwargs.get('ip'),
            reason = kwargs.get('reason', ''),
            data = dict(
                title = old_title,
                content = old_content,
                is_active = old_status,
                tags = list(old_tags)
            )
        )

        has_change = False
        if old_content != self.content:
            has_change = True
            
        if new_tags is not None and old_tags != new_tags: 
            has_change = True
            self.create_tags(new_tags)
            
        if old_title != self.title:
            has_change = True

        if old_status != self.is_active:
            has_change = True

        if has_change:
            self.record(**record_data)

        db_session.commit()  

    @classmethod
    def list(cls, **kwargs):
        json = kwargs.get('json', False)
        order_by = kwargs.get('order', 'date_created DESC')
        articles = cls.query.filter_by(is_active=kwargs.get('is_active')).order_by(order_by).limit(kwargs.get('limit', 10)).offset(kwargs.get('offset', 0)).all()

        if json:
            return [article.json_data() for article in articles]
        return articles


    """
    Count the total number of article
    cache key: article_count:[is_active]
    cache data: int
    """
    @classmethod
    def count(cls, is_active=True):
        return cls.query.filter_by(is_active=is_active).count()

    @classmethod
    def is_owner(cls, id, user_id):
        return cls.query.filter_by(id=id, user_id=user_id).count() == 1

    """
    A convenient method for listing articles and do filtering based on the current user
    """
    @classmethod
    def list_for_user(cls, **kwargs):
        user = kwargs.get('user')
        articles = cls.list(**kwargs)
        if user:
            articles = [user.check_article(article).json_data() for article in articles]
        else:
            articles = [article.json_data() for article in articles]

        return articles

    @classmethod
    def latest_comments(cls, limit=10, offset=0, json=False):
        comments = Comment.query.filter(Comment.article_id != None).order_by('date_created DESC').limit(limit).offset(offset).all()

        if json:
            return [comment.json_data() for comment in comments]

        return comments