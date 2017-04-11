from collections import namedtuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, abort
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from flask import current_app
from app import db
from app.dbmodels.query_role import QueryRole
from app.dbmodels.query_user import QueryUser
from app.dbmodels.query_installation import QueryInstallation
# ===========================


Role = namedtuple(
    'Role',
    ['id', 'name', 'default']
)
# ===========================


class Permission:
    VIEW_REPORT = 0x01          # 0b00000001
    RUN_CASE = 0x02             # 0b00000010
    WRITE_COMMENTS = 0x04       # 0b00000100
    ADMINISTER_EXTERNAL = 0x08  # 0b00001000
    ADMINISTER = 0x80           # 0b10000000

# ===========================


class BaseModel(object):

    def get_by_field(self, name, value):
        kwargs = {name: value}
        modeld = self.query.read_one_by_field(**kwargs)
        if modeld is None:
            abort(404)

        return dict(modeld)
    # ___________________________

    def clear_table(self):
        self.query.remove_all_records()
# ===========================


class RoleModel(BaseModel):

    """

    Columns:
    --------
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)

    # ____________________________

    Roles permissions
    -----------------
    Anonymous       0b00000000 (0x00) # not-logged in - nothing allowed
    ExternalUser    0b00000001 (0x01) # View reports only
    User            0b00000111 (0x07) # View reports, run cases, write comments
    ExternalAdmin   0b00001111 (0xf0) # Administer external users
    Admin           0b11111111 (0xFF) # Administer all

    """
    __tablename__ = 'roles'

    # ____________________________

    def __init__(self):
        self.query = QueryRole(db)
    # ____________________________

    def insert_roles(self):
        """
        """
        roles = {
            'external_user': (Permission.VIEW_REPORT, False),

            'user': (Permission.VIEW_REPORT |
                     Permission.RUN_CASE |
                     Permission.WRITE_COMMENTS, True),

            'external_admin': (
                 Permission.VIEW_REPORT |  # noqa
                 Permission.RUN_CASE |
                 Permission.WRITE_COMMENTS |
                 Permission.ADMINISTER_EXTERNAL, False
            ),

            'admin': (0xff, False)
        }

        for r in roles:
            role = self.query.read_one_by_field(name=r)
            current_app.logger.debug("Role found: %r ", role)
            if role is None:
                role = dict(
                    name=r,
                    permissions=roles[r][0],
                    default=roles[r][1]
                )

                self.query.create(role)

# ===========================


Installation = namedtuple(
    'Installation',
    ['id', 'step', 'step_name']
)


class InstallationModel(BaseModel):
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    display_name = db.Column(db.String(64), unique=True)
    """

    def __repr__(self):
        return '<InstallationStep %r>' % self.name
    # ____________________________

    def __init__(self):
        self.query = QueryInstallation(db)
    # ____________________________

    def insert_steps(self):
        steps = [
            dict(step='hw_config', step_name='HW Config'),
            dict(step='installation', step_name='Installation'),
            dict(step='post_script', step_name='Post Installation Script'),
            dict(step='hw_wizard', step_name='HW Wizard'),
            dict(step='check_all', step_name='Check All'),
            dict(step='direct_io', step_name='Direct IO'),
            dict(step='fc_loopback', step_name='FC Loopback Test'),
            dict(
                step='internal_network',
                step_name='Internal Network Test'
            ),
            dict(step='disable_fc_port', step_name='Disable FC Port'),
            dict(step='mfg_suite', step_name='MFG Test Suite'),
            dict(step='enable_fc_port', step_name='Enable FC Port'),
            dict(step='check_all', step_name='Check All Test'),
            dict(step='cleanup', step_name='Clean Up'),
        ]

        for ind, step in enumerate(steps):
            step['priority'] = ind + 1
            self.query.create(step)
    # ____________________________

    def get_all(self):
        steps = self.query.read()

        # read() returns a list of DictRow objects
        # Casting to a list of dicts
        steps_to_return = [dict(step) for step in steps]
        current_app.logger.debug("Installation steps: %r", steps_to_return)
        return steps_to_return

# ===========================


User = namedtuple(
    'User',
    ['id', 'username', 'email', 'password_hash', 'role', 'permissions']
)
# ____________________________________

AnonymousUser = namedtuple(
    'AnonymousUser',
    []
)
# ____________________________________


class AnonymousUserModel(AnonymousUserMixin):

    # ____________________________

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

            testplan: |testplan_link|
                .. |testplan_link| raw:: html

                   <a href="https://jira.infinidat.com/browse/IVTS-414" target="_blank">IVTS-414</a>

        """
        return False
    # ____________________________

    def is_admin(self):
        return False

# ===========================


class UserModel(UserMixin, BaseModel):

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    """
    # __________________________________

    def __init__(self):
        self.query = QueryUser(db)
    # __________________________________

    @classmethod
    def get_all(cls):
        """
        Fetches all existent users from the DB.

        :Returns:
            A list of User() objects - an object per fetched user.

        """
        cls.set_query()
        user_dicts = cls.query.read()
        return [
            cls().set_user_attributes(user_dict)
            for user_dict in user_dicts
        ]
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
        current_app.logger.info("Current role: %r", self.role)
        return self.userd['role'] is not None and (
            self.userd['permissions'] & permissions) == permissions
    # __________________________________

    def is_admin(self):
        return self.can(Permission.ADMINISTER)
    # __________________________________

    @staticmethod
    def insert_initial_users():
        users = [
            {
                'email': 'bobo@infinidat.com',
                'username': 'bobo',
                'password': '1234'
            },
            {
                'email': 'vziv@infinidat.com',
                'username': 'vziv',
                'password': '1234'
            }
        ]

        for u in users:
            UserModel().save_user(**u)

    # __________________________________

    def save_user(self, email, username, password, role='user'):

        # Set user role
        if role.lower() == 'admin':
            # user is an administrator
            role = RoleModel().get_by_field(name='permissions', value=0xFF)
        else:
            role = RoleModel().get_by_field(name='name', value=role.lower())

        password_hash = generate_password_hash(password)

        new_user_id = self.query.create(
            email=email,
            username=username,
            password_hash=password_hash,
            role_id=role['id']
        )

        print("New user ID: %r" % new_user_id)
        current_app.logger.info("New user ID: %r", new_user_id)

        userd = self.get_by_field(name='id', value=new_user_id)
        return User(**userd)
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

    # ____________________________

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        return User().get_by_field(name='id', value=data['id'])
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
    userd = UserModel().get_by_field(name='id', value=user_id)
    return User(**userd)
