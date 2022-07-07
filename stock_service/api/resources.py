# encoding: utf-8

from flask import request
from flask_restful import Resource

from stock_service.api.schemas import StockSchema
from stock_service.config import URL_EXTERNAL_STOCK

import urllib.request, json, datetime


class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """

    def get(self, stock_code):
        # TODO: Implement the call to the stooq service here. The stock code to query the API
        # should come in a query parameter.
        stock_data_obj = None
        schema = StockSchema()

        url = URL_EXTERNAL_STOCK.format(stock_code)

        response = urllib.request.urlopen(url)
        data = response.read()
        stock_data_obj = json.loads(data)

        stock_data_obj = stock_data_obj['symbols'][0]
        stock_data_obj['date'] = datetime.datetime.strptime(stock_data_obj['date'], "%Y-%m-%d")

        time = datetime.datetime.strptime(stock_data_obj['time'], "%H:%M:%S")
        stock_data_obj['time'] = time.time()
        
        return schema.dump(stock_data_obj)
