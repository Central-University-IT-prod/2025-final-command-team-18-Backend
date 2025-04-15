from flask import Blueprint, jsonify
from schemas import *
from helpers import *
from models import Transaction, Client, Company, Loyal, Activation, HistoryBought
from flask_jwt_extended import (
    decode_token,
)
from flask_pydantic import validate
from werkzeug.exceptions import NotFound
from manage import db

qr_process = Blueprint("qr_process", __name__)


@qr_process.route("/<company_uuid>/register_purchase", methods=["POST"])
@creates_response
@jwt_required()
@check_jwt_access
@validate()
def register_good_transaktion(company_uuid: str, body: RegisterGood):
    companyUUID = CompanyUUID(id=company_uuid).id
    user_id = decode_token(body.qr_data).get("sub")

    client = Client.query.get(user_id)
    if not client:
        print(user_id)
        raise NotFound("No such client")

    company = Company.query.get(companyUUID)
    if not company:
        raise NotFound("No such company")

    for good in body.goods:
        gd = Transaction(
            good_id=good.id, cost=good.cost, company=company, client=client
        )
        his = HistoryBought.query.filter_by(product_id=good.id, company=company).first()
        if his is not None:
            his.count += 1
        else:
            his = HistoryBought(company_id=company_uuid,
                                product_id=good.id, count=1)
            db.session.add(his)
        db.session.add(gd)
    db.session.commit()
    return jsonify({"message": "added"}), 201


@qr_process.route("/<company_uuid>/discount", methods=["GET"])
@creates_response
@jwt_required()
@check_jwt_access
@validate()
def get_discount(company_uuid: str, body: GetDiscount):
    companyUUID = CompanyUUID(id=company_uuid).id
    user_jwt, loyal_id = body.qr_data.split("|")
    user_id = decode_token(user_jwt).get("sub")

    client = Client.query.get(user_id)
    if not client:
        raise NotFound("No such client")

    company = Company.query.get(companyUUID)
    if not company:
        raise NotFound("No such company")

    loyal = Loyal.query.get(loyal_id)
    if not loyal:
        raise NotFound("No such loyal")

    goods_bought = [str(b.id) for b in body.goods]
    print(goods_bought, loyal.permanent_product_id, loyal.accumulate_discount_product_id)
    if not (loyal.permanent_product_id in goods_bought or loyal.accumulate_discount_product_id in goods_bought):
        return jsonify({"error": "No discount items in box"}), 422
    
    if loyal.type == "permanent":
        return (
            jsonify(
                {
                    "discount_product_id": loyal.permanent_product_id,
                    "discount_percent": loyal.permanent_discount_percent,
                }
            ),
            200,
        )

    required_id = loyal.accumulate_product_id
    required_count = loyal.accumulate_n

    activations_query = Activation.query.filter_by(loyal=loyal)
    activ_count = activations_query.count()
    uniq_activ_count = activations_query.filter_by(client=client).count()
    
    bought_count = Transaction.query.filter_by(
        good_id=required_id, client=client, company=company
    ).count()
    if bought_count < required_count:
        return jsonify({"reason": "Not enough products bought"}), 422
    if activ_count > loyal.total_activations:
        return jsonify({"reason": "Already fully activated"}), 422
    if uniq_activ_count > loyal.unique_activations:
        return jsonify({"reason": "You have already fully activated"}), 422

    return (
        jsonify(
            {
                "discount_product_id": loyal.accumulate_discount_product_id,
                "discount_percent": loyal.accumulate_discount_percent,
            }
        ),
        200,
    )


@qr_process.route("/<company_uuid>/discount", methods=["POST"])
@creates_response
@jwt_required()
@check_jwt_access
@validate()
def apply_discount(company_uuid: str, body: GetDiscount):
    companyUUID = CompanyUUID(id=company_uuid).id
    user_jwt, loyal_id = body.qr_data.split("|")
    user_id = decode_token(user_jwt).get("sub")

    client = Client.query.get(user_id)
    if not client:
        raise NotFound("No such client")

    company = Company.query.get(companyUUID)
    if not company:
        raise NotFound("No such company")

    loyal = Loyal.query.get(loyal_id)
    if not loyal:
        raise NotFound("No such loyal")

    goods_bought = [str(b.id) for b in body.goods]
    
    if not (loyal.permanent_product_id in goods_bought or loyal.accumulate_discount_product_id in goods_bought):
        return jsonify({"error": "No discount items in box"}), 422
    
    if loyal.type == "permanent":
        actv = Activation(
            client=client,
            loyal=loyal,
            company_id=companyUUID
        )
        db.session.add(actv)
        his = HistoryBought.query.filter_by(product_id=loyal.permanent_product_id, company=company).first()
        if his is not None:
            his.count += 1
        else:
            his = HistoryBought(company_id=company_uuid,
                                product_id=loyal.permanent_product_id, count=1)
            db.session.add(his)
        db.session.commit()
        return (
            jsonify(
                {
                    "discount_product_id": loyal.permanent_product_id,
                    "discount_percent": loyal.permanent_discount_percent,
                }
            ),
            200,
        )

    required_id = loyal.accumulate_product_id
    required_count = loyal.accumulate_n
    
    activations_query = Activation.query.filter_by(loyal=loyal)
    activ_count = activations_query.count()
    uniq_activ_count = activations_query.filter_by(client=client).count()
    
    bought_count = Transaction.query.filter_by(
        good_id=required_id, client=client, company=company
    ).count()
    if bought_count < required_count:
        return jsonify({"reason": "Not enough products bought"}), 422
    if activ_count > loyal.total_activations:
        return jsonify({"reason": "Already fully activated"}), 422
    if uniq_activ_count > loyal.unique_activations:
        return jsonify({"reason": "You have already fully activated"}), 422
    
    actv = Activation(
        client=client,
        loyal=loyal,
        company_id=company_uuid
    )
    db.session.add(actv)
    his = HistoryBought.query.filter_by(product_id=loyal.accumulate_discount_product_id, company=company).first()
    if his is not None:
        his.count += 1
    else:
        his = HistoryBought(company_id=company_uuid,
                            product_id=loyal.accumulate_discount_product_id, count=1)
        db.session.add(his)
    transactions = Transaction.query.filter_by(
        good_id=required_id, client=client, company=company
    ).all()
    for tr in transactions:
        db.session.delete(tr)
    db.session.commit()

    return (
        jsonify(
            {
                "discount_product_id": loyal.accumulate_discount_product_id,
                "discount_percent": loyal.accumulate_discount_percent,
            }
        ),
        200,
    )
