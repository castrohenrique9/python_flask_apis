# encoding: utf-8

from time import time
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequestKeyError
from api_service.api.schemas import StockInfoSchema, HistoryInfoSchema
from api_service.config import URL_EXTERNAL_STOCK
from api_service.auth import security

from datetime import date, datetime

from urllib.error import URLError
import urllib.request, json

from api_service.api.exceptions import (
    DataNotFoundException,
    GenericException,
    ParameterException,
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

    def get(self):
        data_from_service = None
        schema = StockInfoSchema()

        try:
            data_from_service = StockQuery.get_external_data(request.args["q"])
        except BadRequestKeyError:
            raise ParameterException("Invalid parameter")

        History.save(data_from_service)

        return schema.dump(data_from_service)


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
    def save(cls, data):
        dt = History.convert_date(data["date"])
        tm = History.convert_time(data["time"])
        data["date"] = History.combineDateTime(dt, tm)

        history = models.History(data)
        history.save()

    @classmethod
    def find(cls, user_id):
        history = models.History.find_by_id(user_id)
        return history

    def get(self):
        history = History.find(1)
        schema = HistoryInfoSchema()
        return schema.dump(history)


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """

    def get(self):
        # TODO: Implement this method.
        pass


class UserLogin(Resource):
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
