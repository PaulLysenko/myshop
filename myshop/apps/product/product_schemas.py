from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, ConfigDict, validator


class ProductSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    price: Annotated[Decimal, Field(decimal_places=2, max_digits=12)]
    description: str = ''
    brand: str | None = None

    @field_validator('name')
    def str_validator(cls, value):
        if not value:
            raise ValueError('Empty name')

        value = value.strip()
        if len(value) > 256:
            raise ValueError('Name is too long')

        return value

class ProductValidationSchema(BaseModel):
    name: str
    price: float
    description: str

    @validator("name")
    def validate_name(cls, value):
        if len(value) < 1:
            raise ValueError("Name must be at least 1 character long.")
        return value

    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0.")
        return value

    @validator("description")
    def validate_description(cls, value):
        if len(value) < 1:
            raise ValueError("Description must be at least 1 character long.")
        return value

