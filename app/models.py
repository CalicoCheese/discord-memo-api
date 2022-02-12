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

    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    tos_agree = db.Column(
        db.DateTime,
        nullable=False
    )

    memos = db.relationship("Memo", backref="owner")

    def __repr__(self):
        return f"<User id={self.id}, discord_id={self.discord_id!r}>"


class Memo(db.Model):
    id = db.Column(
        db.Integer,
        unique=True,
        primary_key=True,
        nullable=False
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
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

    def get_edit_timestamp(self):
        return round(self.edit.timestamp)

    def to_json(self):
        return {
            "id": self.id,
            "edit": self.get_edit_timestamp(),
            "text": self.text
        }

    def __repr__(self):
        return f"<Memo id={self.id}, owner_id={self.owner_id}>"


class Notice(db.Model):
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
