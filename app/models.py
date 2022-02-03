from sqlalchemy import func
from app import db


class User(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    discord_id = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    tos_agree = db.Column(
        db.DateTime,
        nullable=False
    )

    def __repr__(self):
        return f"<User id={self.id}, discord_id={self.discord_id!r}>"


class Memo:
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = db.Column(  # User.id
        db.Integer,
        nullable=False
    )

    create = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    edit = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    iv = db.Column(
        db.String(32),
        nullable=False,
    )

    def __repr__(self):
        return f"<Memo id={self.id}, owner_id={self.owner_id}>"


class Notice:
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    """
    Type
        0: notice
        1: privacy
        2: tos(Terms of service)
    """
    type = db.Column(
        db.Integer,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    title = db.Column(
        db.String(40),
        nullable=False,
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<Notice id={self.id}, type={self.type!r}>"
