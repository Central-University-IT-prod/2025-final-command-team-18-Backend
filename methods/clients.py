from helpers import exceptions, IncorrectData
from models import db, Client
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import Conflict, NotFound


def create_client(body):
    if Client.query.filter_by(email=body.email).first():
        raise Conflict('Email already registered')

    password_hash = generate_password_hash(body.password)
    client = Client(name=body.name, surname=body.surname, email=body.email, phone=body.phone,
                    password_hash=password_hash)

    db.session.add(client)
    db.session.commit()

    return client


def get_client_by_email(email):
    client = Client.query.filter_by(email=email).first()
    if client is None:
        raise IncorrectData
    return client