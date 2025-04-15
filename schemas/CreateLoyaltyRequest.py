from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Literal
import re
import base64
from PIL import Image
import io
from datetime import datetime, timezone, timedelta

MSK_TZ = timezone(timedelta(hours=3))


class CreateLoyaltyRequest(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., min_length=5)
    banner: str = Field(...)
    type: Literal["accumulative", "permanent", "ACCUMULATIVE", "PERMANENT"]  # Накопительная и постоянная скидки
    unique_activations: int = Field(..., ge=1)
    total_activations: int = Field(..., ge=1)
    start_date: int = Field(..., ge=0)
    end_date: int = Field(..., ge=0)
    categories: Optional[List[str]] = Field(None, min_length=1)

    accumulate_product_id: str = Field(None)
    accumulate_n: int = Field(None, ge=1)
    accumulate_discount_product_id: str = Field(None)
    accumulate_discount_percent: float = Field(None, ge=0, le=1)

    # Дополнительные поля для типа permanent
    permanent_product_id: str = Field(None)
    permanent_discount_percent: float = Field(None, ge=0, le=1)


    @field_validator("banner")
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

        if width != 300 or height != 200:
            raise ValueError(f"Некорректное соотношение сторон: {width}px:{height}px")

        return value

    @model_validator(mode="after")
    def check_type_of_field(values):
        now_msk = int(datetime.now(MSK_TZ).timestamp())
        if values.type == "accumulative":
            if values.accumulate_product_id is None or values.accumulate_n is None or values.accumulate_discount_product_id is None or values.accumulate_discount_percent is None:
                print(values)
                raise ValueError("Пропущены обязательные поля для типа `накопительные`")
        elif values.type == "permanent":
            if values.permanent_product_id is None or values.permanent_discount_percent is None:
                raise ValueError("Пропущены обязательные поля для типа `постоянные`")

        if values.start_date < now_msk or values.end_date < now_msk:
            raise ValueError("Дата начала не может быть в прошлом")

        if values.start_date > values.end_date:
            raise ValueError("Дата начала не может быть позже конца")

        return values

