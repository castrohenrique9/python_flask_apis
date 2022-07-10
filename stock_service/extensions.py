# encoding: utf-8

from flask_marshmallow import Marshmallow
import pika
from stock_service.config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_VHOST


marsh = Marshmallow()

rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, virtual_host=RABBITMQ_VHOST))
