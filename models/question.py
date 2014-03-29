from flask import url_for

from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.babel import gettext as _
from slugify import slugify

from .database import Base, db_session

from .sphinx import get_sphinx_client
from .answer import Answer

from sqlalchemy import orm

from utils import now_ms, hash, escape

from .mixins.votable import Votable
from .mixins.commentable import Commentable
from .mixins.editable import Editable
from .mixins.taggable import Taggable
from .mixins.pointable import Pointable

class Question(Base, Votable, Commentable, Editable, Taggable, Pointable):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    date_created = Column(BigInteger, default=now_ms)
    content = Column(Text)
    ip = Column(Text)
    answer_count = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('questions', order_by=date_created, cascade='all,delete'))

    user_answer = False

    def json_data(self):
        return {
            "content": escape(self.content),
            "title": self.title,
            "id": self.id,
            "date_created": self.date_created,
            "user": self.user.json_data(),
            "tags": [tag.json_data() for tag in self.tags],
            "points": self.points,
            "comment_count": self.comment_count,
            "user_vote": self.user_vote,
            "user_comment": self.user_comment,
            "user_answer": self.user_answer,
            "answer_count": self.answer_count,
            "urls": self.get_url()
        }

    def get_url(self, name=None):
        urls = {
            'view': url_for('questions.view', slug=slugify(self.title), id=self.id)
        }

        if name:
            return urls.get(name)

        return urls

    def update_answer_count(self, offset=1, commit=False):
        cls = self.__class__
        self.query.filter_by(id=self.id).update({cls.answer_count: cls.answer_count + offset})
        if commit:
            db_session.commit()
        return self.answer_count

    def create_answer(self, content, user, ip, commit=False):
        answer = Answer()
        answer.question_id = self.id
        answer.ip = hash(ip)
        answer.content = content
        answer.user_id = user.id
        db_session.add(answer)
        if commit:
            db_session.commit()
        return answer

    """
    Determine if user has answered or not
    """
    def check_answer(self, user):
        if not user:
            return None

        filter_data = {
            'question_id': self.id,
            'user_id': user.id
        }

        count = Answer.query.filter_by(**filter_data).count()
        self.user_answer = count > 0
        return self.user_answer

    def get_answers(self, limit=10, offset=0, order='date_created desc', json=False):
        filter_data = {
            'question_id': self.id
        }
        
        answers = Answer.query.filter_by(**filter_data).order_by(order).limit(limit).offset(offset).all()
        if json:
            return [answer.json_data() for answer in answers]
        return answers

    @classmethod
    def list(cls, **kwargs):
        json = kwargs.get('json', False)
        order_by = kwargs.get('order', 'date_created DESC')
        questions = cls.query.order_by(order_by).limit(kwargs.get('limit', 10)).offset(kwargs.get('offset', 0)).all()

        if json:
            return [question.json_data() for question in questions]
        return questions

    """
    A convenient method for listing questions and do filtering based on the current user
    """
    @classmethod
    def list_for_user(cls, **kwargs):
        user = kwargs.get('user')
        questions = cls.list(**kwargs)
        if user:
            questions = [user.check_question(question).json_data() for question in questions]
        else:
            questions = [question.json_data() for question in questions]

        return questions