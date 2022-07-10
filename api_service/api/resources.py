# encoding: utf-8

from sqlite3 import IntegrityError
from time import time
from flask import request, jsonify
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequestKeyError
from api_service.api.schemas import (
    StockInfoSchema, 
    HistoryInfoSchema,
    StatsInfoSchema
)

from api_service.config import URL_EXTERNAL_STOCK, RABBITMQ_EXCHANGE
from pika.exceptions import StreamLostError

from api_service.auth import security
from flask_jwt_extended import jwt_required, get_jwt_identity


from datetime import date, datetime

from urllib.error import URLError
import urllib.request, json

from api_service.api.exceptions import (
    DataNotFoundException,
    GenericException,
    ParameterException,
    UnauthorizedException,
)

from api_service import models


attributes = reqparse.RequestParser()


class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """

    @classmethod
    def format_url_external(cls, stock_code: str) -> str:
        try:
            return URL_EXTERNAL_STOCK.format(stock_code)
        except AttributeError:
            raise GenericException(
                "An internal error trying format URL from external resource"
            )

    @classmethod
    def extract_content_external_data(cls, json_load: json):
        """Check external response data"""

        try:
            if json_load["name"]:
                json_load["company_name"] = json_load["name"]
                json_load["quote"] = json_load["close"]
                return json_load
        except KeyError:
            raise DataNotFoundException("Data not found")

    @classmethod
    def get_external_data(cls, stock_code):
        """Request data from external service with URL default"""

        try:
            response = urllib.request.urlopen(
                StockQuery.format_url_external(stock_code)
            )
            data = response.read()
            json_load = json.loads(data)
        except URLError:
            raise GenericException(
                "An error trying request data from external resource"
            )

        return StockQuery.extract_content_external_data(json_load)

    @classmethod
    def publish_queue(cls, user_id: int, stock_code: str):
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
    
    @classmethod
    def listen_queue(cls, data):
        data = json.loads(data)
        try:
            History.save(data["user_id"], data["data"])
        except IntegrityError:
            pass
        
        schema = StockInfoSchema()
        return schema.dump(data["data"])

    @jwt_required()
    def get(self):
        try:
            published = StockQuery.publish_queue(get_jwt_identity(), request.args["q"])
            if published:
                return {"message": "Queue published"}, 200
        except BadRequestKeyError:
            raise ParameterException("Invalid parameter")
        
        raise GenericException("Erro trying publish task in queue")


class History(Resource):
    """
    Returns queries made by current user.
    """

    @classmethod
    def convert_date(cls, date: str, format: str = "%Y-%m-%d") -> datetime.date:
        """Convert date str to date format"""

        try:
            return datetime.strptime(date, format)
        except ValueError:
            raise GenericException("Error to convert date")

    @classmethod
    def convert_time(cls, time: str, format: str = "%H:%M:%S") -> datetime.time:
        """Convert time str to time format"""

        try:
            return datetime.strptime(time, format).time()
        except ValueError:
            raise GenericException("Error to convert date")

    @classmethod
    def combineDateTime(cls, date: date, time: time):
        try:
            return datetime.combine(date, time)
        except AttributeError:
            raise GenericException("An error trying combine date and time")

    @classmethod
    def save(cls, user_id, data):
        dt = History.convert_date(data["date"])
        tm = History.convert_time(data["time"])
        data["date"] = History.combineDateTime(dt, tm)
        data["user_id"] = user_id

        history = models.History(data)
        history.save()

    @classmethod
    def find_by_id(cls, id):
        return models.History.find_by_id(id)

    @classmethod
    def find_all_by_user_id(cls, user_id):
        return models.History.find_all_by_user_id(user_id)

    @classmethod
    def find_stats(cls):
        return models.History.find_stats()

    @jwt_required()
    def get(self):
        histories = History.find_all_by_user_id(get_jwt_identity())
        schema = HistoryInfoSchema()
        histories_dump = [schema.dump(history) for history in histories]
        return histories_dump, 200


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """

    @jwt_required()
    def get(self):
        if UserLogin.is_admin(get_jwt_identity()):
            stats = models.History.find_stats()

            schema = StatsInfoSchema()
            listing = [schema.dump(s) for s in stats]
            return listing, 200
        else:
            raise UnauthorizedException("You are not an administrator")


class UserLogin(Resource):
    @classmethod
    def is_admin(cls, user_id):
        return True if models.User.find_by_id_admin(user_id) else False

    @classmethod
    def post(cls):

        attributes.add_argument(
            "username",
            type=str,
            required=True,
            help="The field 'username' can not be left blank",
        )
        attributes.add_argument(
            "password",
            type=str,
            required=True,
            help="The field 'password' can not be left blank",
        )

        dados = attributes.parse_args()
        return security.authenticate(dados["username"], dados["password"]), 200
