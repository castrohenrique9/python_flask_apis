# encoding: utf-8

from pika.exceptions import (
    StreamLostError,
    ConnectionClosedByBroker
)

from stock_service.api.exceptions import GenericException
from stock_service.api.resources import StockResource

import json

def publish(user_id: int, data):
        """Request data from external service with URL default and RabbitMQ"""
        from stock_service.app import create_rabbitmq_channel_publish
        from stock_service.config import RABBITMQ_EXCHANGE
        
        try:
            rabbitmq_channel = create_rabbitmq_channel_publish()
            # rabbitmq_channel.confirm_delivery()
            rabbitmq_channel.basic_publish(
                exchange=RABBITMQ_EXCHANGE, 
                routing_key="tag_api", 
                body=json.dumps({"user_id": user_id, "data": data})
            )
        
        except StreamLostError:
            raise GenericException(
                "An internal error stream lost"
            )
        except ConnectionClosedByBroker:
            raise GenericException(
                "An internal error because blocker closed connection"
            )
        except Exception as e:
            raise GenericException(
                "An internal error"
            )


def read(user_id: int, stock_code: str):
    stock_data = StockResource.get_stock_data(stock_code)
    publish(user_id, stock_data)
