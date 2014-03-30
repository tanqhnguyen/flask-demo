from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import text

from flask.ext.babel import gettext as _

from .database import Base, db_session, ModelException
from .article import Article
from .question import Question
from .topic import Topic
from .role import Role
from .mixins.pointable import Pointable

from .redis_connection import get_client

from utils import hash, now_ms, unicode_truncate, process_tags_input

class User(Base, Pointable):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128))
    date_created = Column(BigInteger, default=now_ms)
    login_id = Column(Text)
    login_type = Column(String(16))
    access_token = Column(Text)
    social_data = Column(JSON)
    name = Column(String(32))
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text)
    avatar = Column(Text)

    def json_data(self, include_permissions=False):
        data = {
            "id": self.id,
            "name": self.name,
            "login_type": self.login_type,
            "points": self.points
        }

        if include_permissions:
            data['permissions'] = self.get_permissions()

        return data

    def has_permission(self, name):
        permissions = self.get_permissions()
        return name in permissions

    def _permissions_redis_key(self):
        return ":".join(['2', self.__tablename__, str(self.id), 'permissions'])

    def get_permissions(self):
        key = self._permissions_redis_key()
        redis_client = get_client(key)

        if not redis_client.exists(key):   
            command = text("""WITH RECURSIVE recursetree(name, parent) AS (
                                SELECT permissions.name, permissions.parent
                                FROM permissions, roles
                                WHERE roles.user_id = :user_id AND permissions.name = roles.name

                                UNION ALL

                                SELECT p.name, p.parent
                                FROM permissions p JOIN recursetree rt ON rt.name = p.parent
                            )
                            SELECT name FROM recursetree;""")
            
            results = db_session.execute(command, params={'user_id': self.id}).fetchall()

            results = set([result[0] for result in results])
            if len(results) == 0:
                redis_client.sadd(key, '')
            else:   
                redis_client.sadd(key, *results)
        else:
            results = redis_client.smembers(key)

        return list(results)

    def set_role(self, name, commit=False):
        Role.create_or_update(self.id, name)
        key = self._permissions_redis_key()
        redis_client = get_client(key)
        redis_client.delete(key)
        if commit:
            db_session.commit()

    def check_question(self, question):
        question.check_vote(self)
        question.check_comment(self)
        return question

    def check_topic(self, topic):
        topic.check_vote(self)
        topic.check_comment(self)
        return topic

    def create_article(self, title, content, tags, ip):
        article = Article()
        article.title = title
        article.content = content
        article.user_id = self.id
        article.ip = hash(ip)
        db_session.add(article)
        db_session.commit()

        tags = process_tags_input(tags)
        article.create_tags(tags, commit=True)
        return article

    def create_question(self, title, content, tags, ip):
        question = Question()
        question.title = title
        question.content = content
        question.user_id = self.id
        question.ip = hash(ip)
        db_session.add(question)
        db_session.commit()

        tags = process_tags_input(tags)
        question.create_tags(tags, commit=True)
        return question

    def create_topic(self, title, content, tags, ip):
        # verify that the user has not created any topic within the last minute
        last_topic = Topic.query.filter_by(ip=hash(ip)).order_by('date_created DESC').first()

        if last_topic:
            time_diff = now_ms() - last_topic.date_created
            limit = 60*1000 #ms

            if time_diff < limit:
                raise ModelException(
                    type='VALIDATION_FAILED',
                    message=_(u'Please wait %(time)s seconds before creating new topic', time=int(round((limit-time_diff)/1000)))
                )

        topic = Topic()
        topic.title = title
        topic.content = content
        topic.user_id = self.id
        topic.ip = hash(ip)
        db_session.add(topic)
        db_session.commit()

        tags = process_tags_input(tags)
        topic.create_tags(tags, commit=True)
        return topic

    def ban(self, reason, commit=False):
        self.is_banned = True
        self.ban_reason = reason

        if commit:
            db_session.commit()

        return self

    def unban(self, commit=False):
        self.is_banned = False
        self.ban_reason = None
        
        if commit:
            db_session.commit()

        return self

    @classmethod
    def create_or_update(cls, login_id, login_type, social_data, access_token, avatar, email=None, name=None):
        user = cls.query.filter_by(login_id=str(login_id), login_type=login_type).first()
        is_new = False
        if not user:
            is_new = True
            data = {
                'login_id': login_id,
                'login_type': login_type,
                'social_data': social_data,
                'access_token': access_token,
                'email': email,
                'name': unicode_truncate(name, 32),
                'avatar': avatar
            }
            user = cls(**data)

        user.access_token = access_token
        user.social_data = social_data

        db_session.add(user)
        db_session.commit()
        if is_new:
            user.set_role('user', commit=True)
        return user