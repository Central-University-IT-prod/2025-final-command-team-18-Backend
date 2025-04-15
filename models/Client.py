from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Client(db.Model):
    client_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(300), nullable=False)
    surname = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(350), nullable=False)

    def as_dict(self):
        return {
            "client_id": self.client_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone": self.phone
        }
