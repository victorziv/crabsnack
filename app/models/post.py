from app import db
from .base import BaseModel
from app.dbmodels.query_post import QueryPost
# ===========================


class Post(BaseModel):

    """

    Columns:
    --------
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    authorid = db.Column(db.Integer, db.ForeignKey('users.id'))
    """

    __tablename__ = 'posts'
    query = QueryPost(db)

    # ____________________________

    def __init__(self, attrs):
        self.__dict__.update(attrs)
    # ____________________________
