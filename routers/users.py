from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from config import crud, exceptions, hashing
from models import database, models, shcemas


router = APIRouter(
    prefix='/users',
    tags=['user'],
)


@router.post('/admin', response_model=shcemas.AdminRegistration)
def admin_create(
    user: shcemas.AdminRegistration,
    db: Session = Depends(database.get_db)
):
    try:
        admin_model = crud.create_admin(user=user, db=db)
        db.add(admin_model)
        db.commit()
        db.refresh(admin_model)
        return admin_model
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500


@router.post('/create_user', response_model=shcemas.UserUpdate)
def create_user(
    user: shcemas.UserCreate,
    db: Session = Depends(database.get_db)
):
    try:
        user_model = crud.create_new_user(user=user, db=db)
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500
    return user_model


@router.put('/return_user')
def user_return(
    email: str,
    password: str,
    db: Session = Depends(database.get_db)
):
    old_user = crud.get_user_by_email(email, db)
    if not old_user:
        raise exceptions.USER_EXCEPTION_404
    try:
        if email == old_user.email:
            if hashing.Hasher.verify_password(
                password, old_user.hashed_password
            ):
                old_user.is_active = True
                db.commit()
                return {"message": "Пользователь востановлен"}
            else:
                raise exceptions.STRANER_ID_EXEPTION
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500


@router.get('/get/{user_id}', response_model=shcemas.UserSchemas)
def get_user(
    user_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise exceptions.USER_EXCEPTION_404
    return user


@router.get('/get_all/', response_model=list[shcemas.UserSchemas])
def get_all_useres(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    all_users = db.query(models.User).offset(skip).limit(limit).all()
    return all_users


@router.get('/get/my_cats/', response_model=list[shcemas.CatsBase])
def get_all_my_cats(
    user_id: int,
    limit: int = 10,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    cats = db.query(models.Cat).filter(
        models.Cat.owner_id == user_id
    ).limit(limit).all()
    return cats


@router.put("/put/{user_id}", response_model=shcemas.UserSchemas)
def update_user(
    user_id: int,
    upd_user: shcemas.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(crud.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user.is_active:
        raise exceptions.ACTIVE_EXCEPTION_409
    if not user:
        raise exceptions.USER_EXCEPTION_404
    try:
        if current_user.id == user_id or current_user.is_admin:
            user.name = upd_user.name.title()
            user.email = upd_user.email
            db.commit()
            return {'name': upd_user.name.title(), "email": upd_user.email}
        else:
            raise exceptions.STRANER_ID_EXEPTION
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500


@router.delete('/delete/{user_id}')
def delete_user(
    user_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise exceptions.USER_EXCEPTION_404
    try:
        if current_user.id == user_id or current_user.is_admin:
            user.is_active = False
            db.commit()
            return {"message": "Пользователь удален"}
        else:
            raise exceptions.STRANER_ID_EXEPTION
    except SQLAlchemyError:
        raise exceptions.SERVER_EXCEPTION_500
