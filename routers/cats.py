from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import crud, exceptions
from models import database, models, shcemas

router = APIRouter(
    prefix='/cats',
    tags=['cats'],
)


@router.post('/create_cat', response_model=shcemas.Cats)
def create_cat(
    color: shcemas.ColorValidation,
    cat: shcemas.CatsCreate,
    achievment: shcemas.AchievementsBase,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    try:
        user = db.query(models.User).filter(
            models.User.id == current_user.id
        ).first()
        if user.is_active or current_user.is_admin:
            achiev_model = models.Achievement(
                name=achievment.name
            )
            birthday_cat = shcemas.CatsBase.validate_date(cat.birthday)
            cat_model = models.Cat(
                name=cat.name,
                color=color,
                birthday=birthday_cat,
                owner_id=current_user.id,
            )
            if len(achievment.name) == 0:
                db.add(cat_model)
                db.commit()
            else:
                db.add_all([cat_model, achiev_model])
                cat_model.achievements.append(achiev_model)
                db.commit()
            return cat_model
        else:
            raise exceptions.USER_EXCEPTION_404
    except SQLAlchemyError:
        raise exceptions.SERVER_EXCEPTION_500


@router.get('/get/{cat_id}', response_model=shcemas.Cats,)
def get_cat(
    cat_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise exceptions.CAT_EXCEPTION_404
    return cat


@router.put('/update/{cat_id}/', response_model=shcemas.CatsBase)
def update_cat(
    color: shcemas.ColorValidation,
    cat_id: int,
    updated_cat: shcemas.CatsBase,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise exceptions.CAT_EXCEPTION_404
    try:
        if cat.owner_id != current_user.id and not current_user.is_admin:
            raise exceptions.STRANER_ID_EXEPTION
        cat.name = updated_cat.name
        cat.color = color
        cat.birthday = updated_cat.birthday
        db.commit()
        return cat
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500


@router.delete('/delete/{cat_id}')
def delete_cat(
    cat_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise exceptions.CAT_EXCEPTION_404
    try:
        if cat.owner_id != current_user.id and not current_user.is_admin:
            raise exceptions.STRANER_ID_EXEPTION
        db.delete(cat)
        db.commit()
        return {"message": "Котик удален!"}
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500
