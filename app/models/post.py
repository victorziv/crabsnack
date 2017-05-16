from flask import current_app
from app import db
from .base import BaseModel
from app.dbmodels.query_post import QueryPost
from .user import User
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

    def __init__(self, **attrs):
        self.__dict__.update(attrs)
    # ____________________________

    @classmethod
    def get_all(cls, sort_by='postdate', sort_order='desc'):
        post_dicts = cls.query.read(sort_by, sort_order)
        posts = []
        for d in post_dicts:
            d = dict(d)
            post = cls()
            user_attrs = {
                'username': d.pop('username', d['email']),
                'email': d.pop('email'),
                'avatar_hash': d.pop('avatar_hash', '')
            }

            print("USER ATTRS: {}".format(user_attrs))

            post.author = User(attrs=user_attrs)
            post.__dict__.update(d)
            posts.append(post)

        return posts

    # ____________________________

    @classmethod
    def save(cls, body, author):
        new_post_id = cls.query.create(body, author.id)
        current_app.logger.info("New post ID: %r", new_post_id)
        return new_post_id
