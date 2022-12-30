import pydantic

from errors import ApiError


class CreateUserSchema(pydantic.BaseModel):
    email: str
    password: str


class PatchUserSchema(pydantic.BaseModel):
    email: str | None
    password: str | None


class CreateAdvertisementSchema(pydantic.BaseModel):
    title: str
    description: str
    user_id: int


class PatchAdvertisementSchema(pydantic.BaseModel):
    title: str | None
    description: str | None


def validate(data: dict, schema_class):
    try:
        return schema_class(**data).dict()
    except pydantic.ValidationError as err:
        raise ApiError(400, err.errors())
