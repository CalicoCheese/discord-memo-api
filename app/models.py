from sqlalchemy import func
from app import db
from app.aes import decrypt


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

    tos_agree_date = db.Column(
        db.DateTime,
        nullable=False
    )

    privacy_agree_date = db.Column(
        db.DateTime,
        nullable=False
    )

    last_login = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now()
    )

    # memos = db.relationship("Memo", backref="owner")

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

    encrypted = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    def get_edit_timestamp(self):
        return round(self.edit.timestamp())

    def get_text(self):
        return decrypt(payload=self.text)

    def to_json(self):
        return {
            "id": self.id,
            "edit": self.get_edit_timestamp(),
            "text": self.get_text(),
            "encrypted": self.encrypted
        }

    def __repr__(self):
        return f"<Memo id={self.id}, owner_id={self.owner_id}>"


# # # Value for Notice Table # # #
TP_NOTICE = 0
TP_PRIVACY = 1
TP_TOS = 2
TP_LIST = [TP_NOTICE, TP_PRIVACY, TP_TOS]
# # # # # # # # # # # # # # # # #


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

    def get_timestamp(self):
        return round(self.date.timestamp())

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "date": self.get_timestamp(),
            "title": self.title,
            "text": self.text,
        }

    def __repr__(self):
        return f"<Notice id={self.id}, type={self.type!r}>"
