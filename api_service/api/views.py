# encoding: utf-8

from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from api_service.api import resources

from urllib.error import URLError

from api_service.api.exceptions import (
    DataNotFoundException,
    GenericException,
    ParameterException,
    UnauthorizedException,
)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(resources.UserLogin, "/login", endpoint="login")
api.add_resource(resources.StockQuery, "/stock", endpoint="stock")
api.add_resource(resources.History, "/history", endpoint="history")
api.add_resource(resources.Stats, "/stats", endpoint="stats")


@blueprint.errorhandler(ValidationError)
@blueprint.errorhandler(ParameterException)
def handle_marshmallow_error(e):
    return jsonify(e.message), 400

@blueprint.errorhandler(UnauthorizedException)
def handle_error_401(e):
    return jsonify(e.message), 401

@blueprint.errorhandler(URLError)
@blueprint.errorhandler(AttributeError)
@blueprint.errorhandler(DataNotFoundException)
@blueprint.errorhandler(GenericException)
def handle_error_404(e):
    return jsonify(e.message), 404


@blueprint.errorhandler(Exception)
def handle_error_500(e):
    return jsonify({"error": "An internal server error occurred"}), 500
