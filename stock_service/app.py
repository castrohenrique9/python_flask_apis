from flask import Flask
from stock_service import api

from stock_service.extensions import rabbitmq_connection
from stock_service.config import RABBITMQ_EXCHANGE, RABBITMQ_EXCHANGE_TYPE, RABBITMQ_QUEUE_STOCK

from stock_service.api.resources import StockResource

rabbitmq_channel = None

def create_app(testing=False):
    app = Flask("stock_service")
    app.config.from_object("stock_service.config")

    if testing is True:
        app.config["TESTING"] = True

    register_blueprints(app)
    # create_rabbitmq_channel()

    return app


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)

def callback_test(ch, method, properties, body):
    StockResource.get_stock_data(body)


def create_rabbitmq_channel():
    rabbitmq_channel = rabbitmq_connection.channel()
    rabbitmq_channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
    rabbitmq_channel.queue_declare(queue=RABBITMQ_QUEUE_STOCK)
    rabbitmq_channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_STOCK, routing_key="tag_stock")
    
    rabbitmq_channel.basic_consume(queue=RABBITMQ_QUEUE_STOCK, on_message_callback=callback_test, auto_ack=True)
    #rabbitmq_channel.start_consuming()
    return rabbitmq_channel

if __name__ == "__main__":
    app = create_app(False)
    app.run(host="0.0.0.0", port=5001)

    rabbitmq_channel = create_rabbitmq_channel()
    rabbitmq_channel.start_consuming()
