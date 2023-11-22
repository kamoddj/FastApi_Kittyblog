from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config import crud, exceptions
from models import database, models, shcemas

router = APIRouter(
    prefix="/achievements",
    tags=['achievements'],
)


@router.post('/create_achievement', response_model=shcemas.AchievementsBase)
def create_achievement(
    achiev: shcemas.AchievementsBase,
    cat_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise exceptions.CAT_EXCEPTION_404
    if cat.owner_id != current_user.id or not current_user.is_admin:
        raise exceptions.STRANER_ID_EXEPTION
    achiev_model = models.Achievement(
        name=achiev.name
    )
    try:
        db.add(achiev_model)
        cat.achievements.append(achiev_model)
        db.commit()
        db.refresh(achiev_model)
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500
    return achiev_model


@router.get('/get_achievement/{achiev_id}',
            response_model=shcemas.AchievementsBase)
def get_achievements(
    achiev_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    achiev = db.query(models.Achievement).filter(
        models.Achievement.id == achiev_id).first()
    if not achiev:
        raise exceptions.ACHIEV_EXCEPTION_404
    return achiev


@router.get('/get_achievement/', response_model=list[shcemas.Achievements])
def get_all_achievements(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    all_achiev = db.query(models.Achievement).offset(skip).limit(limit).all()
    if not all_achiev:
        exceptions.ACHIEV_EXCEPTION_404
    return all_achiev


@router.put('/update_achievements/{achiev_id}',
            response_model=shcemas.AchievementsBase)
def update_achievements(
    achiev_id: int,
    achiev: shcemas.AchievementsBase,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).join(
        models.Cat).join(models.cat_achievements).filter(
            models.cat_achievements.c.achievement_id == achiev_id).first()
    achiev_new = db.query(models.Achievement).filter(
        models.Achievement.id == achiev_id).first()
    if not achiev_new:
        raise exceptions.ACHIEV_EXCEPTION_404
    try:
        if current_user.id != user.id and not current_user.is_admin:
            raise exceptions.STRANER_ID_EXEPTION
        achiev_new.name = achiev.name
        db.commit()
        return achiev_new
    except SQLAlchemyError:
        raise exceptions.SERVER_EXCEPTION_500


@router.delete('/delete_achievements/{achiev_id}')
def delete_achievements(
    achiev_id: int,
    current_user: models.User = Depends(crud.get_current_user),
    db: Session = Depends(database.get_db)
):
    achiev = db.query(models.Achievement).filter(
        models.Achievement.id == achiev_id).first()
    delete_cat_achievement_query = models.cat_achievements.delete().where(
        (models.cat_achievements.c.achievement_id == achiev_id))
    user = db.query(models.User).join(
        models.Cat).join(models.cat_achievements).filter(
            models.cat_achievements.c.achievement_id == achiev_id).first()
    if not achiev:
        raise exceptions.ACHIEV_EXCEPTION_404
    try:
        if current_user.id != user.id and not current_user.is_admin:
            raise exceptions.STRANER_ID_EXEPTION
        db.execute(delete_cat_achievement_query)
        db.delete(achiev)
        db.commit()
        return {"message": "Достижение удалено!"}
    except SQLAlchemyError:
        db.rollback()
        raise exceptions.SERVER_EXCEPTION_500
