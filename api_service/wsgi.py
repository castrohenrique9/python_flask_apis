from api_service.app import create_app, create_rabbitmq_channel
from api_service.extensions import db

app = create_app()
rabbitmq_channel = create_rabbitmq_channel()
