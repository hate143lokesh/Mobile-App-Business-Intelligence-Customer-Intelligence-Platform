
from pydantic import BaseModel, Field
from typing import Literal


class PredictionInput(BaseModel):

    device_type: int = Field(ge=0, le=2)
    user_type: int = Field(ge=0, le=1)
    marketing_channel: int = Field(ge=0, le=5)

    product_id: int = Field(ge=0)
    product_category: int = Field(ge=0, le=7)

    unit_price: float = Field(gt=0)
    quantity: int = Field(ge=1, le=4)
    discount_percent: int = Field(ge=0, le=30)

    pages_viewed: int = Field(ge=1)
    time_on_site_sec: int = Field(gt=0)
    added_to_cart: int = Field(ge=0, le=1)

    visit_day: int = Field(ge=1, le=31)
    visit_month: int = Field(ge=1, le=12)
    visit_weekday: int = Field(ge=0, le=6)
    visit_season: int = Field(ge=0, le=3)

    session_duration_bucket: Literal[
        "Short", "Very Short", "Long", "Very Long"
    ]

    location: int = Field(ge=0)


class PredictionOutput(BaseModel):

    prediction: int
    prediction_label: str
    purchase_probability: float
    no_purchase_probability: float
