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

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()

        user_count = User.query.read_total()
        current_app.logger.debug("Total users: {}".format(user_count))

        for i in range(user_count):
            u = User.query.read_one_with_offset(offset=randint(0, user_count - 1))
            p = {
                'body': forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                'postdate': forgery_py.date.date(True),
                'authorid': u['id']
            }

            Post.query.create(p)
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
        new_post_id = cls.query.create({'body': body, 'authorid': author.id})
        current_app.logger.info("New post ID: %r", new_post_id)
        return new_post_id
