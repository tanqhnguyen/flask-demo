from sqlalchemy import Column, Integer, String, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import relationship, backref

from .database import Base, db_session
from .tag import Tag

from utils import now_ms

class Edit(Base):
    __tablename__ = 'edits'
    id = Column(Integer, primary_key=True)
    date_created = Column(BigInteger, default=now_ms)
    ip = Column(Text)
    data = Column(JSON)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'))

    user = relationship('User', backref=backref('edits', order_by=date_created, cascade='all,delete'))
    article = relationship('Article', backref=backref('edits', order_by=date_created, cascade='all,delete'))