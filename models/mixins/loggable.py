from models import db_session
from models.redis_connection import get_client

from sqlalchemy import Column, Integer
from utils import now_ms, hash

"""
Provides methods for dealing with log
The target table must have a column view_count INT
"""
class Loggable():
    view_count = Column(Integer, default=0)

    def _last_ip_view(self, ip):
        key = ":".join([self.__tablename__, str(self.id), ip, 'last_view'])
        redis_client = get_client(key)
        last_view = redis_client.getset(key, now_ms())
        if last_view is None:
            last_view = now_ms()
        return int(last_view)

    def _update_user_view_log(self, user_id):
        key = ":".join(["users", str(user_id), "view_log", self.__tablename__])
        redis_client = get_client(key)
        redis_client.zadd(key, now_ms(), self.id)

    def update_view_count(self, ip, user=None, commit=False):
        """Updates the view count of the entry. The view count is only updated once very 2 hours to avoid duplication
        Args:
            ip (str): an ip address of the current user_id
            user (User): the current user (None if it is a guest)
            commit (bool): whether to commit changes
        Returns
            True if view_count is updated
            False otherwise
        """
        updated = False
        last_view = self._last_ip_view(hash(ip))
        threshold = 2*3600*1000 # update view_count once very 2 hours
        diff = now_ms() - last_view
        if diff == 0 or diff > threshold:
            cls = self.__class__
            self.query.filter_by(id=self.id).update({cls.view_count: cls.view_count + 1})
            updated = True
            if commit:
                db_session.commit()

        # add the entry to user log
        if user is not None:
            self._update_user_view_log(user.id)

        return updated