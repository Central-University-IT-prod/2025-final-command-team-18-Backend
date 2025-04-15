from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .Company import Company
from sqlalchemy.dialects.postgresql import JSONB

class Loyal(db.Model):
    loyal_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey(Company.company_id, ondelete="CASCADE"))
    company = db.relationship('Company', foreign_keys=[company_id])
    
    name = db.Column(db.String(300), nullable=False)
    banner = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(150), nullable=False)
    unique_activations = db.Column(db.Integer, nullable=False)
    categories = db.Column(JSONB, nullable=True)
    total_activations = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.BigInteger, nullable=False)
    end_date = db.Column(db.BigInteger, nullable=False)

    description = db.Column(db.Text, nullable=False)

    # Дополнительные поля для типа accumulate
    accumulate_product_id = db.Column(db.String(150), nullable=True)
    accumulate_n = db.Column(db.Integer, nullable=True)
    accumulate_discount_product_id = db.Column(db.String(150), nullable=True)
    accumulate_discount_percent = db.Column(db.Float, nullable=True)

    # Дополнительные поля для типа permanent
    permanent_product_id = db.Column(db.String(150), nullable=True)
    permanent_discount_percent = db.Column(db.Float, nullable=True)

    def as_dict(self):
        result = {
            "loyal_id": self.loyal_id,
            "company_id": self.company_id,
            "name": self.name,
            "banner": self.banner,
            "type": self.type,
            "unique_activations": self.unique_activations,
            "total_activations": self.total_activations,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description
        }
        if self.categories is not None:
            result['categories'] = self.categories
        if self.accumulate_product_id is not None:
            result['accumulate_product_id'] = self.accumulate_product_id
        if self.accumulate_n is not None:
            result['accumulate_n'] = self.accumulate_n
        if self.accumulate_discount_product_id is not None:
            result['accumulate_discount_product_id'] = self.accumulate_discount_product_id
        if self.accumulate_discount_percent is not None:
            result['accumulate_discount_percent'] = self.accumulate_discount_percent

        if self.permanent_product_id is not None:
            result['permanent_product_id'] = self.permanent_product_id
        if self.permanent_discount_percent is not None:
            result['permanent_discount_percent'] = self.permanent_discount_percent

        return result
