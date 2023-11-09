from pydantic import BaseModel


class UserSchemas(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class OwnerSchemas(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AchievementsBase(BaseModel):
    name: str


class Achievements(AchievementsBase):
    id: int

    class Config:
        orm_mode = True


class CatsBase(BaseModel):
    name: str
    color: str
    birthday: int


class CatsCreate(CatsBase):
    pass


class Cats(CatsBase):
    owner: OwnerSchemas
    achievements: list[AchievementsBase] = []

    class Config:
        orm_mode = True


class CatAchiev(BaseModel):
    id: int
