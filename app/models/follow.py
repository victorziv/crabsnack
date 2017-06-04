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
            following_id=self.following.id,
            followed_by_id=self.followed_by.id
        )
        self.query.create(attrs=attrs)
    # ____________________________

    @classmethod
    def remove(cls, f):
        return cls.query.delete(f.following_id, f.followed_by_id)
