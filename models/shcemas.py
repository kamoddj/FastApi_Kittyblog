from typing import Optional
from pydantic import BaseModel, constr


class UserSchemas(BaseModel):
    name: Optional[constr(min_length=1)]
    email: str

    class Config:
        orm_mode = True


class UserUpdate(UserSchemas):
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserSchemas):
    hashed_password: Optional[constr(min_length=8)]


class OwnerSchemas(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AchievementsBase(BaseModel):
    name: Optional[constr(min_length=1)]


class Achievements(AchievementsBase):
    id: int

    class Config:
        orm_mode = True


class CatsBase(BaseModel):
    name: Optional[constr(min_length=1)]
    color: str
    birthday: int


class CatsCreate(CatsBase):
    pass


class Cats(CatsBase):
    owner: OwnerSchemas
    achievements: list[AchievementsBase] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
