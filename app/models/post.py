from flask import abort
from markdown import markdown
import bleach
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
    body Text,
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    authorid = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html Text
    """

    __tablename__ = 'posts'
    query = QueryPost(db)

    # ____________________________

    def __init__(self, **attrs):
        self.__dict__.update(attrs)
    # ____________________________

    @staticmethod
    def compose_posts(post_dicts):
        posts = []
        for d in post_dicts:
            d = dict(d)
            post = Post()

            user_attrs = {
                'username': d.pop('username', d['email']),
                'email': d.pop('email'),
                'avatar_hash': d.pop('avatar_hash', '')
            }
            post.author = User(attrs=user_attrs)
            post.__dict__.update(d)
            posts.append(post)

        return posts
    # ____________________________

    @classmethod
    def get_by_field_or_404(cls, name, value):
        """
        TEMP. till base.get_by_field is fixed
        """
        dicts = cls.query.read_by_field(field_name=name, field_value=value)
        if dicts is None:
            abort(404)

        return cls.compose_posts(dicts)
    # __________________________________

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
    def get_all(cls, sort_by='postdate', sort_order='desc', offset=0, limit=None):
        post_dicts = cls.query.read(sort_by, sort_order, offset, limit)
        return cls.compose_posts(post_dicts)
    # ____________________________

    @staticmethod
    def generate_html_body(body):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', 'p'
        ]

        body_html = bleach.linkify(bleach.clean(
            markdown(body, output_format='html'),
            tags=allowed_tags, strip=True))

        return body_html
    # ____________________________

    @classmethod
    def save(cls, body, author):
        post = {'body': body, 'authorid': author.id}
        post['body_html'] = Post.generate_html_body(body)
        new_post_id = cls.query.create(post)
        current_app.logger.info("New post ID: %r", new_post_id)
        return new_post_id
