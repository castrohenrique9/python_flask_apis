from flask import Flask
from stock_service import api

from stock_service.extensions import rabbitmq_connection
from stock_service.config import RABBITMQ_EXCHANGE, RABBITMQ_EXCHANGE_TYPE, RABBITMQ_QUEUE_STOCK, RABBITMQ_QUEUE_API, RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST

from threading import Thread
import pika
from stock_service.api.resources import StockResource

rabbitmq_channel = None

def create_app(testing=False):
    app = Flask("stock_service")
    app.config.from_object("stock_service.config")

    if testing is True:
        app.config["TESTING"] = True

    register_blueprints(app)

    #create_rabbitmq_channel_publish()
    create_rabbitmq_channel_listen()
    
    return app


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)


def callback(ch, method, properties, body):
    print("Reading queue stock")
    StockResource.get_stock_data(body)
    print("Readed queue stock")


def create_rabbitmq_channel_listen():
    rabbitmq_channel_listen = rabbitmq_connection.channel()
    # rabbitmq_channel_listen.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    rabbitmq_channel_listen.queue_declare(queue=RABBITMQ_QUEUE_STOCK)
    rabbitmq_channel_listen.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_STOCK, routing_key="tag_stock")
    
    rabbitmq_channel_listen.basic_consume(queue=RABBITMQ_QUEUE_STOCK, on_message_callback=callback, auto_ack=True)
    
    thread = Thread(target=rabbitmq_channel_listen.start_consuming)
    thread.start()
    print("Waiting for messages in background")

    return rabbitmq_channel_listen

def create_rabbitmq_channel_publish():
    global rabbitmq_connection

    if not rabbitmq_connection or rabbitmq_connection.is_closed:
        rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host=RABBITMQ_VHOST))
    
    rabbitmq_channel_publish = rabbitmq_connection.channel()
    rabbitmq_channel_publish.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    rabbitmq_channel_publish.queue_declare(queue=RABBITMQ_QUEUE_API)
    rabbitmq_channel_publish.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_API, routing_key="tag_api")
    
    return rabbitmq_channel_publish


if __name__ == "__main__":
    app = create_app(False)
    app.run(host="0.0.0.0", port=5001)

    #rabbitmq_channel_publish = create_rabbitmq_channel_publish()
    #rabbitmq_channel_listen = create_rabbitmq_channel_listen()
    #rabbitmq_channel_listen.start_consuming()
