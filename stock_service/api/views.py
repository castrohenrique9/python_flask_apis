# encoding: utf-8

from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from stock_service.api.resources import StockResource

from urllib.error import URLError

from stock_service.exceptions import DataNotFoundException, GenericException


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(StockResource, "/stock/<string:stock_code>", endpoint="stock")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.message), 400

@blueprint.errorhandler(URLError)
@blueprint.errorhandler(AttributeError)
@blueprint.errorhandler(DataNotFoundException)
@blueprint.errorhandler(GenericException)
def handle_error_404(e):
    return jsonify(e.message), 404

@blueprint.errorhandler(Exception)
def handle_error_500(e):
    return jsonify({"error": "An internal server error occurred"}), 500


