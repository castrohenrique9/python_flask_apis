"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

URL_EXTERNAL_STOCK = os.getenv("URL_EXTERNAL_STOCK")
QUERY_ROW_LIMIT_DEFAULT = os.getenv("QUERY_ROW_LIMIT_DEFAULT", default=5)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", default="127.0.0.1")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", default="5672")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", default="/")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", default="guest")
RABBITMQ_PWD = os.getenv("RABBITMQ_PWD", default="guest")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", default="jobsity")
RABBITMQ_EXCHANGE_TYPE = os.getenv("RABBITMQ_EXCHANGE_TYPE", default="direct")
RABBITMQ_QUEUE_STOCK = os.getenv("RABBITMQ_QUEUE_STOCK", default="stock_service")
RABBITMQ_QUEUE_API = os.getenv("RABBITMQ_QUEUE_API", default="api_service")
