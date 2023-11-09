from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    date = Column(DateTime)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)


class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Cat(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(String)
    birthday = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", backref="cats")

    achievements = relationship("Achievement", secondary="cat_achievements")


cat_achievements = Table(
    'cat_achievements', Base.metadata,
    Column('cat_id', Integer, ForeignKey('cats.id')),
    Column('achievement_id', Integer, ForeignKey('achievements.id'))
)
