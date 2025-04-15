from models import db, Loyal, Company
from sqlalchemy import func
from werkzeug.exceptions import NotFound
from datetime import datetime
from . import save_base64_image
from sqlalchemy import cast, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import or_, and_


def create_loyalties_method(body, company_id):
    path = save_base64_image(body.banner)
    loyal = Loyal(company_id=company_id, name=body.name, banner=path, type=body.type, unique_activations=body.unique_activations,
                  categories=body.categories, total_activations=body.total_activations, start_date=body.start_date,
                  end_date=body.end_date, description=body.description)

    if body.type == "accumulative":
        loyal.accumulate_product_id = body.accumulate_product_id
        loyal.accumulate_n = body.accumulate_n
        loyal.accumulate_discount_product_id = body.accumulate_discount_product_id
        loyal.accumulate_discount_percent = body.accumulate_discount_percent

    elif body.type == "permanent":
        loyal.permanent_product_id = body.permanent_product_id
        loyal.permanent_discount_percent = body.permanent_discount_percent

    db.session.add(loyal)
    db.session.commit()

    return loyal


def get_categories_method():
    loyals = Loyal.query.all()
    categories = []
    for loyal in loyals:
        for category in loyal.categories:
            categories.append(category)

    return list(set(categories))


def get_loyalties_method(query):
    query_db = db.session.query(Loyal)

    if query.categories is not None:
        category_list = [cat.strip() for cat in query.categories.split(",")]
        print(category_list)
        query_db = query_db.filter(
            and_(
                Loyal.categories.isnot(None),
                Loyal.categories != cast([], JSONB),
                or_(*(Loyal.categories.op("@>")(cast([cat], JSONB)) for cat in category_list))
            )
        )

    if query.company is not None:
        query_db = query_db.join(Company).filter(Company.company_id == query.company)

    loyalties = query_db.limit(query.limit).offset(query.offset).all()
    loyalties = [lol.as_dict() for lol in loyalties]
    return loyalties


def get_loyalty_by_id(loyal_id):
    loyal = Loyal.query.filter_by(loyal_id=loyal_id).first()

    if loyal is None:
        raise NotFound("loyal not found")

    return loyal


def patch_loyalty_by_id(loyal, body):
    if body.unique_activations is not None:
        loyal.unique_activations = body.unique_activations
    if body.total_activations is not None:
        loyal.total_activations = body.total_activations
    if body.end_date is not None and body.end_date >= datetime.timestamp(datetime.now()):
        loyal.end_date = body.end_date

    db.session.commit()

    return loyal


def delete_loyalty_by_id(loyal_id):
    loyal = Loyal.query.filter_by(loyal_id=loyal_id).first()

    if loyal is None:
        raise NotFound("loyal not found")

    db.session.delete(loyal)
    db.session.commit()

    return "ok"
