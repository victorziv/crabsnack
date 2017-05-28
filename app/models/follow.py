from app import db
from .base import BaseModel
from app.dbmodels.query_follow import QueryFollow
# ===========================


class Follow(BaseModel):

    __tablename__ = 'follow'
    query = QueryFollow(db)

    # ____________________________

    def __init__(self, follower, followed):
        self.follower = follower
        self.followed = followed
    # ____________________________

    def save(self):
        attrs = dict(
            follower_id=self.follower.id,
            followed_id=self.followed.id
        )
        self.query.create(attrs=attrs)
