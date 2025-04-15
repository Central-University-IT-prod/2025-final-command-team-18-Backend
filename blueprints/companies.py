from flask import Blueprint, jsonify, request
from schemas import *
from methods import create_company, get_company_by_email, get_all_companies_method
from helpers import *
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, create_refresh_token, unset_jwt_cookies
from werkzeug.security import check_password_hash
from flask_pydantic import validate
from werkzeug.exceptions import  BadRequest

company = Blueprint('company', __name__)


@company.route("/register", methods=['POST'])
@creates_response
@validate()
def create_companies(body: CreateCompanyRequest):
    company = create_company(body)

    return jsonify(company.as_dict()), 201


@company.route("/login", methods=["POST"])
@creates_response
def login():
    data = request.json

    if 'email' not in data or 'password' not in data:
        raise BadRequest('Missing email or password')

    company1 = get_company_by_email(data['email'])

    if not check_password_hash(company1.password_hash, data['password']):
        raise IncorrectData


    access_token = create_access_token(identity=company1.company_id, additional_claims={"user_id": company1.company_id, "access": "admin"})

    # redis_client.setex(f"refresh:{company1.company_id}", 2592000, refresh_token)

    return jsonify({"jwt": access_token, "company_id": company1.company_id}), 200


@company.route("/companies", methods=["GET"])
@creates_response
@validate()
def get_all_companies(query: PaginationRequest):
    companies = get_all_companies_method(query)

    return jsonify(companies), 200
