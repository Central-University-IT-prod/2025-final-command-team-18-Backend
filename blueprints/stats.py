from flask import Blueprint, jsonify, request, make_response
from schemas import *
from methods import get_max_activated, get_total_count, get_loyal_product_count, get_categories_usages
from helpers import *
from werkzeug.exceptions import  BadRequest, NotFound
from models import Company

stats = Blueprint('stats', __name__)


@stats.route("/<company_id>/max/activated", methods=["GET"])
@creates_response
@jwt_required()
@check_jwt_access
def get_max_activated_loyalties(company_id):
    if company_id is None:
        raise BadRequest("company_id is required")

    company = Company.query.filter_by(company_id=company_id).first()
    if company is None:
        raise NotFound("Company not found")


    activated_loyalties = get_max_activated(company_id)

    return jsonify(activated_loyalties), 200


@stats.route("/<company_id>/count/product", methods=["GET"])
@creates_response
@jwt_required()
@check_jwt_access
def get_product_total_count(company_id):
    if company_id is None:
        raise BadRequest("company_id is required")
    company = Company.query.filter_by(company_id=company_id).first()
    if company is None:
        raise NotFound("Company not found")

    total_count = get_total_count(company_id)

    return jsonify(total_count), 200


@stats.route("/<company_id>/count/loyalty/product", methods=["GET"])
@creates_response
@jwt_required()
@check_jwt_access
def get_product_loyalty_count(company_id):
    if company_id is None:
        raise BadRequest("company_id is required")
    company = Company.query.filter_by(company_id=company_id).first()
    if company is None:
        raise NotFound("Company not found")

    total_count = get_loyal_product_count(company_id)

    return jsonify(total_count), 200


@stats.route("/<company_id>/categories/usage", methods=["GET"])
@creates_response
@jwt_required()
@check_jwt_access
def get_category_usage(company_id):
    if company_id is None:
        raise BadRequest("company_id is required")
    company = Company.query.filter_by(company_id=company_id).first()
    if company is None:
        raise NotFound("Company not found")

    category_usages = get_categories_usages(company_id)

    return jsonify(category_usages), 200
