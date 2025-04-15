from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Company(db.Model):
    company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    vertical_banner = db.Column(db.String(300), nullable=True)
    password_hash = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(350), nullable=False)

    def as_dict(self):
        return {
            "company_id": self.company_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "image_url": self.vertical_banner,
        }
