from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from uuid import UUID


class Good(BaseModel):
    id: str = Field(...)
    cost: float = Field(...)


class RegisterGood(BaseModel):
    qr_data: str = Field(...)
    goods: List[Good] = Field(...)
    
    @field_validator("qr_data")
    def validate_qr(cls, value):
        lv = value.split("/")
        if len(lv) != 2:
            raise ValueError("QR should have 2 parts")
        
        if lv[0] != "individual":
            raise ValueError("Wrong qr type")
        return lv[1]


class GetDiscount(BaseModel):
    qr_data: str = Field(...)
    goods: List[Good] = Field(...)
    
    @field_validator("qr_data")
    def validate_qr(cls, value):
        lv = value.split("/")
        if len(lv) != 3:
            raise ValueError("QR should have 2 parts")
        
        if lv[0] != "loyal":
            raise ValueError("Wrong qr type")
        return "|".join(lv[1:])
