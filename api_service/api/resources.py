from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequestKeyError
from api_service.api.schemas import StockInfoSchema
from api_service.extensions import db

from urllib.error import URLError
import urllib.request, json, datetime

from api_service.api.exceptions import (
    DataNotFoundException,
    GenericException,
    ParameterException,
)


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
            if json_load[0]["name"]:
                return json_load[0]
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

        return schema.dump(data_from_service)


class History(Resource):
    """
    Returns queries made by current user.
    """
    def get(self):
        # TODO: Implement this method.
        pass


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    def get(self):
        # TODO: Implement this method.
        pass
