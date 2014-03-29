from models import db_session, ModelException

from sqlalchemy import Column, Integer
from flask.ext.babel import gettext as _
from utils import hash, get_remote_side, get_remote_side_class, now_ms
from models.redis_connection import get_client


"""
Provides methods for dealing with comment
The target table must have a column comment_count INT
"""
class Commentable():
    user_comment = False
    
    comment_limit = 30*1000 #ms

    comment_count = Column(Integer, default=0)

    def update_comment_count(self, offset=1, commit=False):
        cls = self.__class__
        self.query.filter_by(id=self.id).update({cls.comment_count: cls.comment_count + offset})

        if commit:
            db_session.commit()

        return self.comment_count 

    def _comment_count_redis_key(self, user_id):
        return ':'.join([self.__tablename__, str(self.id), 'user_comment_count', str(user_id)])

    def update_user_comment_count(self, user_id, offset=1):
        key = self._comment_count_redis_key(user_id)
        redis_client = get_client(key)
        if offset > 0:
            result = redis_client.incr(key, offset)
        else:
            result = redis_client.decr(key, abs(offset))
        return int(result)

    """
    Determine if user has commented or not
    """
    def check_comment(self, user):
        if not user:
            return None

        key = self._comment_count_redis_key(user.id)
        redis_client = get_client(key)

        if not redis_client.exists(key):
            ref_name = get_remote_side(self, 'comments')
            filter_data = {
                ref_name: self.id,
                'user_id': user.id
            }
            cls = get_remote_side_class(self, 'comments')
            count = cls.query.filter_by(**filter_data).count()
            redis_client.set(key, count)
        else:
            count = redis_client.get(key)

        count = int(count)
        self.user_comment = count > 0
        return self.user_comment

    """
    Get comments of the article
    cache key: article:[article_id]:comments
    cache data: array of comments
    cache type: sorted set
    """
    def get_comments(self, limit=10, offset=0, order='date_created desc', json=False):
        ref_name = get_remote_side(self, 'comments')

        filter_data = {
            ref_name: self.id
        }
        cls = get_remote_side_class(self, 'comments')
        comments = cls.query.filter_by(**filter_data).order_by(order).limit(limit).offset(offset).all()
        if json:
            return [comment.json_data() for comment in comments]
        return comments

    def create_comment(self, content, user, ip, commit=False):
        ref_name = get_remote_side(self, 'comments')
        
        cls = get_remote_side_class(self, 'comments')

        # verify that the user has not created any comment for this article within the last 30s
        # TODO: cache this shit
        last_comment = cls.query.filter_by(ip=hash(ip)).order_by(cls.date_created.desc()).first()

        if last_comment:
            time_diff = now_ms() - last_comment.date_created
            limit = self.comment_limit

            if time_diff < limit:
                raise ModelException(
                    type='VALIDATION_FAILED',
                    message=_(u'Please wait %(time)s seconds before sending new comment', time=int(round((limit-time_diff)/1000)))
                )

        comment = cls()
        setattr(comment, ref_name, self.id)
        comment.user_id = user.id
        comment.content = content
        comment.ip = hash(ip)

        # also update the comment count
        key = self._comment_count_redis_key(user.id)
        redis_client = get_client(key)
        redis_client.incr(key)

        db_session.add(comment)

        if commit:
            db_session.commit()

        return comment