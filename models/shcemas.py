from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr

from config.exceptions import CAT_EXCEPTION_409


# Validations
class ColorValidation(str, Enum):
    black = 'black'
    white = 'white'
    grey = 'grey'
    ginger = 'ginger'


# User Schems
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


class AdminRegistration(UserCreate):
    is_admin: bool


class OwnerSchemas(BaseModel):
    name: str

    class Config:
        orm_mode = True


# Achievements Schems
class AchievementsBase(BaseModel):
    name: str
    # name: Optional[constr(min_length=1)]


class Achievements(AchievementsBase):
    id: int

    class Config:
        orm_mode = True


# Cats Schems
class CatsBase(BaseModel):
    name: Optional[constr(min_length=1)]
    color: ColorValidation
    birthday: int

    def validate_date(birthday):
        date = datetime.now()
        now = int(date.strftime('%Y'))
        if (now - birthday) > 18:
            raise CAT_EXCEPTION_409
        return birthday


class CatsCreate(CatsBase):
    pass


class Cats(CatsBase):
    owner: OwnerSchemas
    achievements: list[AchievementsBase] = []

    class Config:
        orm_mode = True


# Token Schems
class Token(BaseModel):
    access_token: str
    token_type: str
