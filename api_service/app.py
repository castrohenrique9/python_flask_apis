# encoding: utf-8

from flask import Flask
from flask_jwt_extended import JWTManager
from api_service import api
from api_service.extensions import db, rabbitmq_connection
from api_service.extensions import migrate

from api_service.config import RABBITMQ_EXCHANGE, RABBITMQ_EXCHANGE_TYPE, RABBITMQ_QUEUE_STOCK

rabbitmq_channel = None


def create_app(testing=False):
    app = Flask("api_service")
    app.config.from_object("api_service.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    create_jwt(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)


def create_jwt(app):
    jwt = JWTManager(app)
    return jwt


def create_rabbitmq_channel():
    rabbitmq_channel = rabbitmq_connection.channel()
    rabbitmq_channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    rabbitmq_channel.queue_declare(queue=RABBITMQ_QUEUE_STOCK)
    rabbitmq_channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_STOCK, routing_key="tag_stock")
    
    return rabbitmq_channel
