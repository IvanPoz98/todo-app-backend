from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    is_active: bool


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'