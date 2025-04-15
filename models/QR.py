from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .Company import Company
from .Client import Client
from .Loyal import Loyal

class Transaction(db.Model):
    transaction_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    good_id = db.Column(db.String(150), nullable=False)
    
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Company.company_id, ondelete="CASCADE"))
    company = db.relationship('Company', foreign_keys='Transaction.company_id')
    
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Client.client_id, ondelete="CASCADE"))
    client = db.relationship('Client', foreign_keys='Transaction.client_id')
    
    cost = db.Column(db.Float, nullable=False)

class Activation(db.Model):
    activation_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    loyal_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Loyal.loyal_id, ondelete="CASCADE"))
    loyal = db.relationship('Loyal', foreign_keys='Activation.loyal_id')
    
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Client.client_id, ondelete="CASCADE"))
    client = db.relationship('Client', foreign_keys='Activation.client_id')

    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Company.company_id, ondelete="CASCADE"))
    company = db.relationship('Company', foreign_keys='Activation.company_id')
