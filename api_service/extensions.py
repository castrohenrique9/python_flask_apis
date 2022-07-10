# encoding: utf-8

from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

import pika
from api_service.config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST, RABBITMQ_EXCHANGE, RABBITMQ_EXCHANGE_TYPE, RABBITMQ_QUEUE_STOCK

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host=RABBITMQ_VHOST))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type=RABBITMQ_EXCHANGE_TYPE)
rabbitmq_channel.queue_declare(queue=RABBITMQ_QUEUE_STOCK)
rabbitmq_channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE_STOCK, routing_key="tag_stock")

