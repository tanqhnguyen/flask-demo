from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from .database import Base, db_session

class Role(Base):
    __tablename__ = 'roles'
    name = Column(String(32), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

    user = relationship('User', backref=backref('role', cascade='all,delete', uselist=False))

    @classmethod
    def create_or_update(cls, user_id, name, commit=False):
        role = cls.query.filter_by(user_id=user_id, name=name).first()
        if not role:
            role = cls()
            role.user_id = user_id
            role.name = name
        else:
            role.name = name

        db_session.add(role)
        if commit:
            db_session.commit()
        return role
