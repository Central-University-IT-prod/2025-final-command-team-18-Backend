from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

from schemas import *
from methods import *
from helpers import *
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from schemas import PatchLoyaltyRequest

loyal = Blueprint('loyal', __name__)


@loyal.route("/create/loyalty", methods=["POST"])
@creates_response
@jwt_required()
@check_jwt_access
@validate()
def create_loyalties(body: CreateLoyaltyRequest):
    current_user = get_jwt()
    company = Company.query.filter_by(company_id=current_user["user_id"]).first()
    if company is None:
        raise NotFound("Company not found")
    loyal = create_loyalties_method(body, current_user["user_id"])
    return jsonify(loyal.as_dict()), 201


@loyal.route("/categories", methods=["GET"])
@creates_response
@validate()
def get_categories():
    categories = get_categories_method()
    sorted_categories = sorted(categories)
    return sorted_categories, 200


@loyal.route("/loyalties", methods=["GET"])
@creates_response
@validate()
def get_loyalties(query: PaginationRequest):
    loyalties = get_loyalties_method(query)
    return jsonify(loyalties), 200


@loyal.route("/loyalty/<loyalty_id>", methods=["GET"])
@creates_response
def get_loyalty(loyalty_id):
    loyalty = get_loyalty_by_id(loyalty_id)

    return jsonify(loyalty.as_dict()), 200


@loyal.route("/loyalty/<loyalty_id>", methods=["PATCH"])
@creates_response
@validate()
@jwt_required()
@check_jwt_access
def patch_loyalty(loyalty_id, body: PatchLoyaltyRequest):
    current_user = get_jwt()
    company = Company.query.filter_by(company_id=current_user["user_id"]).first()
    if company is None:
        raise NotFound("Company not found")
    loyalty = get_loyalty_by_id(loyalty_id)
    loyalty_patch = patch_loyalty_by_id(loyalty, body)

    return jsonify(loyalty_patch.as_dict()), 200


@loyal.route("/loyalty/<loyalty_id>", methods=["DELETE"])
@creates_response
@jwt_required()
@check_jwt_access
def delete_loyalty(loyalty_id):
    current_user = get_jwt()
    company = Company.query.filter_by(company_id=current_user["user_id"]).first()
    if company is None:
        raise NotFound("Company not found")
    print(loyalty_id)
    message = delete_loyalty_by_id(loyalty_id)

    return jsonify({
        'status': message
    }), 204

