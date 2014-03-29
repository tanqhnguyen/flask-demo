from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from .database import Base, db_session

from utils import now_ms

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    date_created = Column(BigInteger, default=now_ms)
    up = Column(Boolean, default=True)
    ip = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
    answer_id = Column(Integer, ForeignKey('answers.id', ondelete='CASCADE'))
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('votes', order_by=date_created, cascade='all,delete'))
    article = relationship('Article', backref=backref('votes', order_by=date_created, cascade='all,delete'))
    question = relationship('Question', backref=backref('votes', order_by=date_created, cascade='all,delete'))
    answer = relationship('Answer', backref=backref('votes', order_by=date_created, cascade='all,delete'))
    topic = relationship('Topic', backref=backref('votes', order_by=date_created, cascade='all,delete'))

    @classmethod
    def create_or_update(cls, **kwargs):
        commit = kwargs.get('commit', False)
        ip = kwargs.get('ip')
        up = kwargs.get('up')
        
        foreign_keys = ['user_id', 'article_id', 'question_id', 'answer_id', 'topic_id']

        filters = dict()
        for key in foreign_keys:
            data = kwargs.get(key)
            if data:
                filters[key] = data

        vote = cls.query.filter_by(**filters).first()

        if not vote:
            vote = cls()
            for key in foreign_keys:
                data = kwargs.get(key)
                if data:
                    setattr(vote, key, data)

            vote.ip = ip

        if vote.up != up:
            vote.changed = True
        else:
            vote.changed = False

        vote.up = up
        db_session.add(vote)

        if commit:
            db_session.commit()

        return vote