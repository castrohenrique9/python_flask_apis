# encoding: utf-8

from sqlalchemy.ext.hybrid import hybrid_property
from api_service.extensions import db, pwd_context

from flask import jsonify


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username


class History(db.Model):
    """History model"""

    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(True), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    open = db.Column(db.Float(precision=2), nullable=False)
    high = db.Column(db.Float(precision=2), nullable=False)
    low = db.Column(db.Float(precision=2), nullable=False)
    close = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, date, name, symbol, open, high, low, close):
        self.date = date
        self.name = name
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __repr__(self) -> str:
        return jsonify(
            date=self.date,
            name=self.name,
            symbol=self.symbol,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
        )
