from flask import current_app
from app import db
from .base import BaseModel, Permission
from app.dbmodels.query_role import QueryRole
# ===========================


class Role(BaseModel):

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
    Moderator       0b00001111 (0xf0) # Administer external users
    Admin           0b11111111 (0xFF) # Administer all

    """
    __tablename__ = 'roles'
    query = QueryRole(db)

    # ____________________________

    def __init__(self, attrs):
        self.query = QueryRole(db)
        self.__dict__.update(attrs)
    # ____________________________

    @classmethod
    def insert_roles(cls):
        """
        Create a new role only if not already in DB.
        Otherwise - update.
        """
        roles = {
            'external_user': (
                Permission.FOLLOW, False),

            'user': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),

            'moderator': (
                Permission.FOLLOW |
                Permission.COMMENT |
                Permission.WRITE_ARTICLES |
                Permission.MODERATE_COMMENTS, False),

            'admin': (0xff, False)
        }

        for r in roles:
            role = cls.query.read_one_by_field(name=r)
            current_app.logger.debug("Role found: %r ", role)
            if role is None:
                role = dict(
                    name=r,
                    permissions=roles[r][0],
                    isdefault=roles[r][1]
                )

                cls.query.create(role)
            else:
                role['permissions'] = roles[r][0],
                role['isdefault'] = roles[r][1]
                cls.query.update(role)
# ===========================
