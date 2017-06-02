from app import dba
from .base import BaseModel
from app.dbmodels.query_follow import QueryFollow
from .user import User
# ===========================


class Follow(BaseModel):

    __tablename__ = 'follow'
    query = QueryFollow(dba)

    # ____________________________

    @classmethod
    def get_followers_for(cls, user, limit=None, offset=None):
        followers_dicts = cls.query.read(
            followed_id=user.id,
            offset=offset,
            limit=limit
        )

        followers = [User(attrs) for attrs in followers_dicts]

        return followers

    # ____________________________

    def save(self):
        attrs = dict(
            follower_id=self.follower.id,
            followed_id=self.followed.id
        )
        self.query.create(attrs=attrs)
    # ____________________________

    @classmethod
    def remove(cls, f):
        return cls.query.delete(f.follower_id, f.followed_id)
