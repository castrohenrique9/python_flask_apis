# encoding: utf-8

from flask import request
from flask_restful import Resource

from stock_service.api.schemas import StockSchema

import urllib.request, json


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

        url = 'https://stooq.com/q/l/?s={}&f=sd2t2ohlcvn&h&e=json'.format(stock_code)

        response = urllib.request.urlopen(url)
        data = response.read()
        stock_data_obj = json.loads(data)
        
        #return schema.dump(stock_data_obj)
        return stock_data_obj
