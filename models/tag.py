from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from .database import Base, db_session

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'))

    article = relationship('Article', backref=backref('tags', order_by=name, cascade='all,delete'))
    question = relationship('Question', backref=backref('tags', order_by=name, cascade='all,delete'))
    topic = relationship('Topic', backref=backref('tags', order_by=name, cascade='all,delete'))

    def json_data(self):
        return {
            "name": self.name
        }

    @classmethod
    def autocomplete(cls, query):
        query = query.lower()
        command = "SELECT name, count(name) as count FROM tags WHERE name LIKE '%%{0}%%' GROUP BY name ORDER BY count DESC LIMIT 10".format(query)
        results = db_session.execute(command)
        data = list()
        for result in results:
            data.append({
                "name": result[0],
                "count": result[1]
            })

        return data