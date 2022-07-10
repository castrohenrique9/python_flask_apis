# encoding: utf-8

from flask import Flask
from flask_jwt_extended import JWTManager
from api_service import api
from api_service.api.resources import StockQuery
from api_service.extensions import db, rabbitmq_connection
from api_service.extensions import migrate

from threading import Thread
import pika
from api_service.config import RABBITMQ_EXCHANGE, RABBITMQ_EXCHANGE_TYPE, RABBITMQ_QUEUE_STOCK, RABBITMQ_QUEUE_API, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST

rabbitmq_channel = None


def create_app(testing=False):
    app = Flask("api_service")
    app.config.from_object("api_service.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)
    
    create_jwt(app)

    #create_rabbitmq_channel_publish()
    create_rabbitmq_channel_listen()

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)


def create_jwt(app):
    jwt = JWTManager(app)
    return jwt


def callback(ch, method, properties, body):
    StockQuery.listen_queue(body)


def create_rabbitmq_channel_listen():
    rabbitmq_channel_listen = rabbitmq_connection.channel()
    #rabbitmq_channel_listen.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    rabbitmq_channel_listen.queue_declare(queue=RABBITMQ_QUEUE_API)
    rabbitmq_channel_listen.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_API, routing_key="tag_api")
    
    rabbitmq_channel_listen.basic_consume(queue=RABBITMQ_QUEUE_API, on_message_callback=callback, auto_ack=True)
    
    thread = Thread(target=rabbitmq_channel_listen.start_consuming)
    thread.start()
    print("Waiting for messages in background tag_api")

    return rabbitmq_channel_listen


def create_rabbitmq_channel_publish():
    global rabbitmq_connection

    if not rabbitmq_connection or rabbitmq_connection.is_closed:
        rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host=RABBITMQ_VHOST))
    
    rabbitmq_channel_publish = rabbitmq_connection.channel()
    rabbitmq_channel_publish.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    rabbitmq_channel_publish.queue_declare(queue=RABBITMQ_QUEUE_STOCK)
    rabbitmq_channel_publish.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_STOCK, routing_key="tag_stock")
    
    return rabbitmq_channel_publish
