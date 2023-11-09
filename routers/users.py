from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.database import get_db
from models.models import User, Cat

from models.shcemas import UserSchemas, CatsBase
from config.conf import SERVER_EXCEPTION_500, USER_EXCEPTION_404


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('/create_user',
             response_model=UserSchemas,
             description="Добавление пользователя по ID")
def create_user(user: UserSchemas, db: Session = Depends(get_db)):
    try:
        user_model = User(
            name=user.name,
            email=user.email
        )
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
    except SQLAlchemyError:
        db.rollback()
        raise SERVER_EXCEPTION_500
    return user_model


@router.get('/get/{user_id}', response_model=UserSchemas)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise USER_EXCEPTION_404
    return user


@router.get('/get_all/', response_model=list[UserSchemas])
def get_all_useres(skip: int = 0,
                   limit: int = 100,
                   db: Session = Depends(get_db)):
    all_users = db.query(User).offset(skip).limit(limit).all()
    return all_users


@router.get('/get/my_cats/', response_model=list[CatsBase])
def get_all_my_cats(user_id: int,
                    limit: int = 10,
                    db: Session = Depends(get_db)):
    cats = db.query(Cat).filter(Cat.owner_id == user_id).limit(limit).all()
    return cats


@router.put("/put/{user_id}", response_model=UserSchemas)
def update_user(user_id: int,
                upd_user: UserSchemas,
                db: Session = Depends(get_db)
                ):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise USER_EXCEPTION_404
    try:
        user.name = upd_user.name
        user.email = upd_user.email
        db.commit()
        return {'name': upd_user.name, "email": upd_user.email}
    except SQLAlchemyError:
        db.rollback()
        raise SERVER_EXCEPTION_500


@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise USER_EXCEPTION_404
    try:
        db.delete(user)
        db.commit()
        return {"message": "Пользователь удален"}
    except SQLAlchemyError:
        raise SERVER_EXCEPTION_500
