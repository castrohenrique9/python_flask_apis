# encoding: utf-8

from sqlalchemy.ext.hybrid import hybrid_property
from api_service.extensions import db, pwd_context

from flask import jsonify


class User(db.Model):
    """Basic user model"""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    

    @classmethod
    def find_by_username(cls, username: str):
        user = cls.query.filter_by(username=username).first()
        return user if user else None

    @classmethod
    def find_by_id(cls, id: int):
        user = cls.query.filter_by(id=id).first()
        return user if user else None

    @classmethod
    def find_by_id_admin(cls, id: int):
        user = cls.query.filter_by(id=id, role="ADMIN").first()
        return user if user else None

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

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    date = db.Column(db.DateTime(True), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    open = db.Column(db.Float(precision=2), nullable=False)
    high = db.Column(db.Float(precision=2), nullable=False)
    low = db.Column(db.Float(precision=2), nullable=False)
    close = db.Column(db.Float(precision=2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, data):
        self.date = data["date"]
        self.name = data["name"]
        self.symbol = data["symbol"]
        self.open = data["open"]
        self.high = data["high"]
        self.low = data["low"]
        self.close = data["close"]
        self.user_id = data["user_id"]

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

    @classmethod
    def find_by_id(cls, id):
        history = cls.query.filter_by(id=id).first()
        return history if history else None

    @classmethod
    def find_all_by_user_id(cls, user_id):
        history = cls.query.filter_by(user_id=user_id).order_by(History.date.desc()).all()
        return history if history else None

    @classmethod
    def find_stats(cls):
        stock = History.symbol.label("stock")
        return db.session.query(stock, db.func.count(History.symbol).label("times_requested")).group_by(History.symbol).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
