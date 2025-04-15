from pydantic import BaseModel, Field, field_validator, EmailStr
import base64
from PIL import Image
import io
from pydantic_extra_types.phone_numbers import PhoneNumber
import phonenumbers
import re



class CompanyUUID(BaseModel):
    id: str = Field(...)


class CreateCompanyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    phone: PhoneNumber = Field(...)
    email: EmailStr = Field(..., min_length=8, max_length=120)
    password: str = Field(..., min_length=8, max_length=60)
    vertical_banner: str = Field(...)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        special_characters = r"!@#$%^&*()_+{}[]\\|/.<>,\"';:~`-*"
        allowed_characters = special_characters + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if not (8 <= len(value) <= 60 and any(c.isupper() for c in value) and any(c.islower() for c in value) and any(
                c.isdigit() for c in value) and any(c in special_characters for c in value) and all(c in allowed_characters for c in value)):
            raise ValueError('Password incorrect')
        return value

    @field_validator("vertical_banner")
    @classmethod
    def validate_vertical_banner(cls, value):
        if not value.startswith("data:image/"):
            raise ValueError("Некорректный формат изображения")

        base64_pattern = r"^data:image\/[a-zA-Z]*;base64,[A-Za-z0-9+/=]*$"
        if not re.match(base64_pattern, value):
            raise ValueError("Некорректный формат base64 для изображения")

        base64_data = value.split(",")[1]
        image_data = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(image_data))

        width, height = image.size

        if width != 140 or height != 180:
            raise ValueError(f"Некорректное соотношение сторон: {width}px:{height}px")

        return value

    @field_validator("phone", mode='after')
    def format_phone(cls, value):
        if isinstance(value, str):
            parsed_number = phonenumbers.parse(value, None)
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        return value