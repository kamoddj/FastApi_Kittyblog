from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.database import get_db
from models.models import Cat, Achievement, User

from models.shcemas import Cats, CatsBase, CatsCreate, AchievementsBase
from config.exceptions import SERVER_EXCEPTION_500, CAT_EXCEPTION_404


router = APIRouter(
    prefix='/cats',
    tags=['cats'],
)


@router.post('/create_cat',
             response_model=Cats,
             description="Добавление котика по ID")
def create_cat(user_id: int,
               cat: CatsCreate,
               achievment: AchievementsBase,
               db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user.is_active:
            achiev_model = Achievement(
                name=achievment.name
            )
            cat_model = Cat(
                name=cat.name,
                color=cat.color,
                birthday=cat.birthday,
                owner_id=user_id,
            )
            db.add_all([cat_model, achiev_model])
            cat_model.achievements.append(achiev_model)
            db.commit()
            return cat_model
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Пользователь удален!'
            )
    except SQLAlchemyError:
        raise SERVER_EXCEPTION_500


@router.get('/get/{cat_id}',
            response_model=Cats,
            description="Получение котика по ID")
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if not cat:
        raise CAT_EXCEPTION_404
    return cat


@router.put('/put/{cat_id}/',
            response_model=CatsBase,
            description="Редактирование котика по ID")
def update_cat(
    cat_id: int,
    updated_cat: CatsBase,
    db: Session = Depends(get_db)
     ):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if not cat:
        raise CAT_EXCEPTION_404
    try:
        cat.name = updated_cat.name
        cat.color = updated_cat.color
        cat.birthday = updated_cat.birthday
        db.commit()
        return cat
    except SQLAlchemyError:
        db.rollback()
        raise SERVER_EXCEPTION_500


@router.delete('/delete/{cat_id}',
               description="Удаление котика по ID")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    if not cat:
        raise CAT_EXCEPTION_404
    try:
        db.delete(cat)
        db.commit()
        return {"message": "Котик удален!"}
    except SQLAlchemyError:
        db.rollback()
        raise SERVER_EXCEPTION_500
