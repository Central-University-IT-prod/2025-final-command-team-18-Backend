from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime, timezone, timedelta

MSK_TZ = timezone(timedelta(hours=3))


class PatchLoyaltyRequest(BaseModel):
    unique_activations: Optional[int] = Field(None, ge=1)
    total_activations: Optional[int] = Field(None, ge=1)
    end_date: Optional[int] = Field(None, ge=1)

    @model_validator(mode="after")
    def check_type_of_field(values):
        now_msk = int(datetime.now(MSK_TZ).timestamp())
        if values.end_date is not None:
            if values.end_date < now_msk:
                raise ValueError("Дата начала не может быть в прошлом")

        return values
