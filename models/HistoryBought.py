from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .Company import Company


class HistoryBought(db.Model):
    history_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Company.company_id, ondelete="CASCADE"))
    company = db.relationship('Company', foreign_keys='HistoryBought.company_id')

    product_id = db.Column(db.String(500), nullable=False)
    count = db.Column(db.Integer, nullable=False)
