from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper
from sqlalchemy.ext.declarative import declarative_base
import config

connect_string = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (config.POSTGRES['username'], config.POSTGRES['password'], config.POSTGRES['host'], config.POSTGRES['port'], config.POSTGRES['database'])

# config.ENV != 'production'
engine = create_engine(connect_string, convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

DeclarativeBase = declarative_base()
DeclarativeBase.query = db_session.query_property()

class ModelException(Exception):
    def __init__(self, message, type):
        Exception.__init__(self, message)
        self.type = type

class Base(DeclarativeBase):
    __abstract__ = True
    # __table_args__ = {"useexisting": True}

    def delete(self, commit=False):
        db_session.delete(self)
        if commit:
            db_session.commit()

    def _redis_key(self, pk):
        return ":".join(self.__tablename__, pk)

    @classmethod
    def find_by_pk(cls, pk):
        pk_name = class_mapper(cls).primary_key[0].name    
        query = {pk_name: pk}
        return cls.query.filter_by(**query).first()