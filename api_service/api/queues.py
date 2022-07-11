# encoding: utf-8

import json

from sqlite3 import IntegrityError

from sqlalchemy.exc import IntegrityError
from api_service.api.schemas import StockInfoSchema

from api_service.config import RABBITMQ_EXCHANGE

from api_service.api.exceptions import GenericException
from pika.exceptions import StreamLostError
from urllib.error import URLError

def publish(user_id: int, stock_code: str):
    """Request data from external service with URL default and RabbitMQ"""
    from api_service.app import create_rabbitmq_channel_publish
    try:
        data = {"user_id": user_id, "stock_code": stock_code}
        data = json.dumps(data)

        rabbitmq_channel_publish = create_rabbitmq_channel_publish()
        rabbitmq_channel_publish.basic_publish(exchange=RABBITMQ_EXCHANGE, routing_key="tag_stock", body=data)
    except URLError:
        raise GenericException("An error trying publish queue")
    except StreamLostError:
        raise GenericException("An error of Stream lost")

    return True


def read(data):
    from api_service.api.resources import History
    
    data = json.loads(data)
    try:
        History.save(data["user_id"], data["data"])
    except IntegrityError:
        pass
    
    schema = StockInfoSchema()
    return schema.dump(data["data"])
