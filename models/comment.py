from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from .database import Base, db_session

from utils import now_ms, hash, escape

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    date_created = Column(BigInteger, default=now_ms)
    content = Column(Text)
    ip = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
    answer_id = Column(Integer, ForeignKey('answers.id', ondelete='CASCADE'))
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('comments', order_by=date_created, cascade='all,delete'))
    article = relationship('Article', backref=backref('comments', order_by=date_created, cascade='all,delete'))
    question = relationship('Question', backref=backref('comments', order_by=date_created, cascade='all,delete'))
    answer = relationship('Answer', backref=backref('comments', order_by=date_created, cascade='all,delete'))
    topic = relationship('Topic', backref=backref('comments', order_by=date_created, cascade='all,delete'))

    def json_data(self):
        return dict(
            id = self.id,
            content = escape(self.content),
            date_created = self.date_created,
            user = self.user.json_data()
        )