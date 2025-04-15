from models import Activation, db, HistoryBought, Loyal
from sqlalchemy import or_
from sqlalchemy import func, cast


def get_max_activated(company_id):
    activations = db.session.query(Activation.loyal_id, db.func.count(Activation.activation_id)) \
        .filter_by(company_id=company_id) \
        .group_by(Activation.loyal_id) \
        .all()

    result = []
    for loyal_id, count in activations:
        if count > 0:
            result.append({"loyal_id": loyal_id, "count": count})

    return result


def get_total_count(company_id):
    products = HistoryBought.query.filter_by(company_id=company_id).all()
    result = []
    for product in products:
        result.append({"product_id": product.product_id,"count": product.count})

    return result


def get_loyal_product_count(company_id):
    products = HistoryBought.query.filter_by(company_id=company_id).all()
    result = []
    for product in products:
        prod = Loyal.query.filter(
            or_(
                Loyal.accumulate_product_id == product.product_id,
                Loyal.permanent_product_id == product.product_id
            )
        ).first()
        if prod is not None:
            result.append({"product_id": product.product_id,"count": product.count})

    return result


def get_categories_usages(company_id):
    category_usage = (
        db.session.query(
            func.jsonb_each_text(Loyal.categories).label("category"),
            func.count(Activation.activation_id).label("usage_count")
        )
        .join(Activation, Activation.loyal_id == Loyal.loyal_id)
        .filter(Activation.company_id == company_id)
        .group_by("category")
        .all()
    )

    result = [{"category": cat, "usage_count": count} for cat, count in category_usage]

    return result
