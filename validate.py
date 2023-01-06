from pydantic import BaseModel, ValidationError
from errors import ApiError
from typing import Optional, Any, Dict


class CreateUserSchema(BaseModel):
    email: str
    password: str


class PatchUserSchema(BaseModel):
    email: Optional[str]
    password: Optional[str]


class CreateAdvertisementSchema(BaseModel):
    title: str
    description: str
    user_id: int


class PatchAdvertisementSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]


def validate(data: Dict[str, Any], schema_class, exclude_none: bool = True) -> dict:
    try:
        return schema_class(**data).dict(exclude_none=exclude_none)
    except ValidationError as err:
        raise ApiError(400, err.errors())
