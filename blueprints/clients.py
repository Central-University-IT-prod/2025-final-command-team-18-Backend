from flask import Blueprint, jsonify, request, make_response
from schemas import *
from methods import create_client, get_client_by_email
from helpers import *
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, unset_jwt_cookies
from manage import redis_client
import datetime
from werkzeug.security import check_password_hash
from flask_pydantic import validate
from werkzeug.exceptions import BadRequest

client = Blueprint('client', __name__)


@client.route("/register", methods=['POST'])
@creates_response
@validate()
def create_clients(body: CreateClientRequest):
    client = create_client(body)

    return jsonify(client.as_dict()), 201


@client.route("/login", methods=["POST"])
@creates_response
def login():
    data = request.json

    if 'email' not in data or 'password' not in data:
        raise BadRequest('Missing email or password')

    client = get_client_by_email(data['email'])

    if not check_password_hash(client.password_hash, data['password']):
        raise IncorrectData

    access_token = create_access_token(identity=client.client_id, additional_claims={"user_id": client.client_id, "access": "client"})

    # redis_client.setex(f"refresh:{client.client_id}", 2592000, refresh_token)

    return jsonify({"jwt": access_token, "client_id": client.client_id}), 200
