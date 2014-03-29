from models import db_session

from sqlalchemy import Column, Integer

"""
Provides methods for dealing with points
The target table must have a column points INT
"""
class Pointable():
    points = Column(Integer, default=0) 

    def update_points(self, up=True, points=1, commit=False):
        if not up:
            points = -points
        cls = self.__class__
        self.query.filter_by(id=self.id).update({cls.points: cls.points + points})
        if commit:
            db_session.commit()

        return self.points