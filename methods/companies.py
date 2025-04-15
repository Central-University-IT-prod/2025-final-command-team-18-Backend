from models import db, Company
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import Conflict
import base64
import os
import io
from PIL import Image
from config import UPLOADFLOADER, SERVER_ADD
import string
import random
from helpers import *
from flask import url_for


def save_base64_image(base64_string):
    if not base64_string.startswith("data:image/"):
        raise ValueError("Некорректный формат base64 (ожидается data:image/...)")

    base64_data = base64_string.split(",")[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data))
    os.makedirs(UPLOADFLOADER, exist_ok=True)
    file_extension = base64_string.split(";")[0].split("/")[-1]
    characters = string.ascii_letters + string.digits
    filename = ''.join(random.choices(characters, k=30))

    file_path = os.path.join(UPLOADFLOADER, f"{filename}.{file_extension}")

    if file_extension == 'gif':
        image.save(file_path, save_all=True)
    else:
        image.save(file_path)

    path = url_for('serve_image', filename=f"{filename}.{file_extension}", _external=True)
    res = path.split('/images')
    res1 = res[0] + SERVER_ADD + "/" + UPLOADFLOADER + res[1]

    return str(res1)


def create_company(body):
    if Company.query.filter_by(email=body.email).first():
        raise Conflict('Email already registered')

    file_path = save_base64_image(body.vertical_banner)
    password_hash = generate_password_hash(body.password)

    company = Company(name=body.name, email=body.email, phone=body.phone, vertical_banner=file_path,
                    password_hash=password_hash)

    db.session.add(company)
    db.session.commit()

    return company


def get_company_by_email(email):
    company = Company.query.filter_by(email=email).first()
    if company is None:
        raise IncorrectData
    return company


def get_all_companies_method(query):
    companies = Company.query.limit(query.limit).offset(query.offset).all()
    companies = [company.as_dict() for company in companies]

    return companies
