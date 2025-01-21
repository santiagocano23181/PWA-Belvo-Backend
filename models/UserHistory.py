from datetime import datetime, timedelta
from sqlalchemy import event, DDL
from .User import User
from utils.db import db


class UserHistory(db.Model):
    __tablename__ = 'userHistory'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('userHistory', lazy=True))

    event_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    event_data = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id: int, event_data: str) -> None:
        actual = datetime.now()
        self.event_date = actual
        self.event_data = event_data
        self.user_id = user_id
