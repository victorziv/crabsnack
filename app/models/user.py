import hashlib
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, request
from flask_login import UserMixin, AnonymousUserMixin
from .. import login_manager
from flask import current_app
from app import dba
from app.dbmodels.query_user import QueryUser
from .role import Role
from .base import BaseModel, Permission
from .follow import Follow
# ===========================


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        """Fake permissions check for an anonymous user.

        An anonymous user is not going to have permissions to do anything in our environment.

        :Steps:
            #. We are generally repelled by the folks
                that don't care to introduce themselves properly.
            #. It's even worse when they do it on the phone.

        :Args:
            permissions (int): Permissions mask as an integer number.

        :Returns:
            bool: Always return False no matter how hard you've been asked to approve.

        :Attributes:
            ticket: |ticket_link|
                .. |ticket_link| raw:: html

                   <a href="https://jira.infinidat.com/browse/IVTS-415" target="_blank">IVTS-415</a>

        """
        return False
    # ____________________________

    def is_administrator(self):
        return False
# ===========================


class User(UserMixin, BaseModel):

    """
    __tablename__ = 'users'

    """
    query = QueryUser(dba)

    # __________________________________

    def __init__(self, attrs={}):
        self.__dict__.update(attrs)
        self.query = QueryUser(dba)

    # __________________________________

    @classmethod
    def get_all(cls):
        """
        Fetches all existent users from the DB.

        :Returns:
            A list of User() objects - an object per fetched user.

        """
        user_dicts = cls.query.read()
        return [
            cls().set_user_attributes(user_dict)
            for user_dict in user_dicts
        ]
    # ____________________________

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(attrs=dict(follower=self, followed=user))
            Follow.save(f)
    # ____________________________

    def is_following(self, user):
        return Follow.get_by_field(name='followed_id', value=user.id) is not None
    # ____________________________

    def gravatar(self, size=100, default='identicon', rating='g'):

        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'

        current_app.logger.info("Avatar hash: {}".format(self.avatar_hash))
        print("Avatar hash: {}".format(self.avatar_hash))
        if self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
            User.update_user(params={'email': self.email, 'avatar_hash': self.avatar_hash})

        return '{url}/{checksum}?s={size}&d={default}&r={rating}'.format(
            url=url, checksum=self.avatar_hash, size=size, default=default, rating=rating)
    # ____________________________

    def to_json(self):

        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

        return json_user

    # __________________________________

    def can(self, permissions):
        """
        Figures out whether the current role can do anything
        given a set of permissions to check against.

        :Returns:
            bool : True or False

        """
        current_app.logger.info("User {} role: {}".format(self.email, self.role))
        return self.role is not None and (
            self.permissions & permissions) == permissions
    # __________________________________

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    # __________________________________

    @staticmethod
    def insert_initial_users():
        users = [
            {
                'email': 'victor_ziv@yahoo.com',
                'username': 'Bobo Mintz',
                'password': '1234'
            },
            {
                'email': 'ziv.victor@gmail.com',
                'username': 'Donald Duck',
                'role': 'admin',
                'password': '1234'
            },
            {
                'email': 'victor@colabo.com',
                'username': 'External Creature',
                'role': 'external_user',
                'password': '1234'
            }
        ]

        for u in users:
            User.save(u)

    # __________________________________

    def save_user_oauth(self, email, username, social_id, role='user'):

        # Set user role
        if role.lower() == 'admin':
            # user is an administrator
            role = Role.get_by_field(name='permissions', value=0xFF)
        else:
            role = Role.get_by_field(name='name', value=role.lower())

        current_app.logger.info(("Role: {}".format(role)))

        new_user_id = self.query.create_oauth(
            email=email,
            username=username,
            social_id=social_id,
            role_id=str(role.id)
        )

        current_app.logger.info("New user ID: %r", new_user_id)
        user = User.get_by_field(name='id', value=new_user_id)
        return user
    # ____________________________

    @classmethod
    def save(cls, attrs):
        role = attrs.pop('role', 'user')
        password = attrs.pop('password')
        email = attrs['email']
        attrs['username'] = attrs.get('username', attrs['email'])

        # Set user role
        if role.lower() == 'admin':
            # user is an administrator
            role = Role.get_by_field(name='permissions', value=0xFF)
        else:
            role = Role.get_by_field(name='name', value=role.lower())

        attrs['role_id'] = str(role.id)
        attrs['password_hash'] = generate_password_hash(password)

        attrs['avatar_hash'] = hashlib.md5(email.encode('utf-8')).hexdigest()

        new_user_id = cls.query.create(attrs)

        current_app.logger.info("New user ID: %r", new_user_id)
        return cls.get_by_field(name='id', value=new_user_id)
    # ____________________________

    def exists_by_username(self, username):
        userd = self.query.read_one_by_field(username=username)
        if userd:
            return True
        else:
            return False
    # ____________________________

    def exists_by_email(self, email):
        userd = self.query.read_one_by_field(email=email)
        if userd:
            return True
        else:
            return False
    # ____________________________

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})
    # __________________________________

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py
        seed()

        for i in range(count):
            u = dict(
                email=forgery_py.internet.email_address(),
                username=forgery_py.name.full_name(),
                password=forgery_py.lorem_ipsum.word(),
                location=forgery_py.address.city(),
                about_me=forgery_py.lorem_ipsum.sentence(),
                member_since=forgery_py.date.date(True))

            User.save(u)
    # __________________________________

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        self.query.update(
            update_key_name='email',
            update_key_value=self.email,
            update_params={'last_seen': self.last_seen})
    # __________________________________

    @classmethod
    def update_user(cls, params):
        cls.query.update(
            update_key_name='email',
            update_key_value=params.pop('email'),
            update_params=params)
    # __________________________________

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        return User.get_by_field(name='id', value=data['id'])
    # ____________________________

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # __________________________________

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    # __________________________________

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

# ===========================


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_field(name='id', value=user_id)
