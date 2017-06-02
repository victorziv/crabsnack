from app import dba
from .base import BaseModel
from app.dbmodels.query_follow import QueryFollow
# ===========================


class Follow(BaseModel):

    __tablename__ = 'follow'
    query = QueryFollow(dba)

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
