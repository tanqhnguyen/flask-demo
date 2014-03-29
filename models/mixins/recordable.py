from utils import get_remote_side, get_remote_side_class, hash

from models import db_session

class Recordable():
    def record(self, user, ip, data, reason=None, commit=False):
        ref_name = get_remote_side(self, 'edits')

        cls = get_remote_side_class(self, 'edits')
        edit = cls()
        setattr(edit, ref_name, self.id)
        edit.user_id = user.id
        edit.ip = hash(ip)
        edit.data = data
        edit.reason = reason

        db_session.add(edit)

        if commit:
            db_session.commit()