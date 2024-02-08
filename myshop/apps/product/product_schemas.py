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
    description: str
    price: float

    @validator("name")
    def validate_name(cls, value):
        if len(value) < 1:
            raise ValueError("Error name length. Add at least 1 character.")
        return value

    @validator("description")
    def validate_description(cls, value):
        if len(value) < 1:
            raise ValueError("Error description length. Add at least 1 character.")
        return value

    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Error price value. Price must be higher than zero.")
        return value


