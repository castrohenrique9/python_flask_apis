# encoding: utf-8

from urllib.error import URLError
from flask import request
from flask_restful import Resource

from stock_service.api.schemas import StockSchema
from stock_service.config import URL_EXTERNAL_STOCK

import urllib.request, json, datetime

from stock_service.exceptions import DataNotFoundException, GenericException


class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """

    
    @classmethod
    def format_url_external(cls, stock_code: str) -> str:
        try:
            return URL_EXTERNAL_STOCK.format(stock_code)
        except AttributeError:
            raise GenericException("An internal error trying format URL from external resource")

    @classmethod
    def get_external_data(cls, stock_code):
        """Request data from external service with URL default"""
        result: json

        try:
            response = urllib.request.urlopen(StockResource.format_url_external(stock_code))
            data = response.read()
            json_load = json.loads(data)
        except URLError:
            raise GenericException("An error trying request data from external resource")
        
        try:
            result = json_load["symbols"][0]
        except KeyError:
            raise DataNotFoundException("Data not found")

        return result

    @classmethod
    def convert_date(cls, date: str, format: str = "%Y-%m-%d") -> datetime.date:
        """Convert date str to date format"""

        try:
            return datetime.datetime.strptime(date, format)
        except ValueError:
            raise GenericException("Error to convert date")
    
    @classmethod
    def convert_time(cls, time: str, format: str = "%H:%M:%S") -> datetime.time:
        """Convert time str to time format"""

        try:
            return datetime.datetime.strptime(time, format).time()
        except ValueError:
            raise GenericException("Error to convert date")

    def get(self, stock_code: str):
        stock_data_obj = None
        schema = StockSchema()

        stock_data_obj = StockResource.get_external_data(stock_code)
        
        stock_data_obj["date"] = StockResource.convert_date(stock_data_obj["date"])
        stock_data_obj["time"] = StockResource.convert_time(stock_data_obj["time"])

        return schema.dump(stock_data_obj)
