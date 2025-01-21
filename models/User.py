from utils.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
