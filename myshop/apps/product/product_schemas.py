from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, ConfigDict


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
