from utils import hash, get_remote_side, get_remote_side_class
from models.redis_connection import get_client

class Votable():
    user_vote = None

    def _user_vote_redis_key(self, user_id):
        return ':'.join([self.__tablename__, str(self.id), 'user_vote', str(user_id)])

    """
    vote up = 1
    vote down = -1
    no vote = 0
    """
    def _vote_value_for_redis(self, vote):
        if vote:
            if vote.up:
                return 1
            else:
                return -1
        else:
            return 0

    """
    Reverse of _vote_value_for_redis
    """
    def _parse_vote_value_from_redis(self, value):
        if value == 0:
            return None
        else:
            return value == 1

    def _update_vote_value_for_redis(self, user_id, vote):
        key = self._user_vote_redis_key(user_id)
        redis_client = get_client(key)
        redis_client.set(key, self._vote_value_for_redis(vote))

    """
    Determine if user_id has voted or not
    """
    def check_vote(self, user):
        ref_name = get_remote_side(self, 'votes')
        if not user:
            self.user_vote = None
            return self.user_vote
        
        key = self._user_vote_redis_key(user.id)
        redis_client = get_client(key)

        if not redis_client.exists(key):
            filter_data ={
                ref_name: self.id,
                'user_id': user.id
            }
            cls = get_remote_side_class(self, 'votes')
            vote = cls.query.filter_by(**filter_data).first()

            if vote:
                self.user_vote = vote.up
            else:
                self.user_vote = None

            redis_client.set(key, self._vote_value_for_redis(vote))
        else:
            value = int(redis_client.get(key))
            self.user_vote = self._parse_vote_value_from_redis(value)

        return self.user_vote

    def vote(self, user, ip, up=True, commit=False):
        ref_name = get_remote_side(self, 'votes')
        cls = get_remote_side_class(self, 'votes')

        data = {
            "user_id": user.id,
            ref_name: self.id,
            "up": up,
            "ip": hash(ip),
            "commit": commit
        }

        vote = cls.create_or_update(**data)
        self._update_vote_value_for_redis(user.id, vote)

        return vote

    def unvote(self, user, commit=False):
        ref_name = get_remote_side(self, 'votes')
        cls = get_remote_side_class(self, 'votes')

        data = {
            ref_name: self.id,
            "user_id": user.id
        }

        vote = cls.query.filter_by(**data).first()

        if vote:
            vote.delete(commit=commit)

        self._update_vote_value_for_redis(user.id, None)

        return vote

