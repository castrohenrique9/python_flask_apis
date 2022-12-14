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
