from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
import phonenumbers
from typing import Optional


class CreateClientRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    surname: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: PhoneNumber
    email: EmailStr = Field(..., min_length=8, max_length=120)
    password: str = Field(..., min_length=8, max_length=60)


    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        special_characters = r"!@#$%^&*()_+{}[]\\|/.<>,\"';:~`-*"
        allowed_characters = special_characters + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if not (8 <= len(value) <= 60 and any(c.isupper() for c in value) and any(c.islower() for c in value) and any(
                c.isdigit() for c in value) and any(c in special_characters for c in value) and all(c in allowed_characters for c in value)):
            raise ValueError('Password incorrect')
        return value

    @field_validator("phone", mode='after')
    def format_phone(cls, value):
        if isinstance(value, str):
            parsed_number = phonenumbers.parse(value, None)
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        return value

