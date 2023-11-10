from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.shcemas import AchievementsBase, Achievements
from models.database import get_db
from models.models import Achievement, Cat

from config.exceptions import SERVER_EXCEPTION_500, ACHIEV_EXCEPTION_404


router = APIRouter(
    prefix="/achievements",
    tags=['achievements'],
)


@router.post('/create_achievement',
             response_model=AchievementsBase,
             description="Добавление достижения по ID")
def create_achievement(achiev: AchievementsBase,
                       cat_id: int,
                       db: Session = Depends(get_db)):
    cat = db.query(Cat).filter(Cat.id == cat_id).first()
    achiev_model = Achievement(
        name=achiev.name
    )
    try:
        db.add(achiev_model)
        cat.achievements.append(achiev_model)
        db.commit()
        db.refresh(achiev_model)
    except SQLAlchemyError:
        db.rollback()
        raise SERVER_EXCEPTION_500
    return achiev_model


@router.get('/get_achievement/{achiev_id}',
            response_model=AchievementsBase,
            description="Получение достижения по ID")
def get_achievements(achiev_id: int, db: Session = Depends(get_db)):
    achiev = db.query(Achievement).filter(Achievement.id == achiev_id).first()
    if not achiev:
        raise ACHIEV_EXCEPTION_404
    return achiev


@router.get('/get_achievement/',
            response_model=list[Achievements],
            description="Просмотр всех существующих достижений, "
            "можно выставить лимит.")
def get_all_achievements(skip: int = 0,
                         limit: int = 10,
                         db: Session = Depends(get_db)):
    all_achiev = db.query(Achievement).offset(skip).limit(limit).all()
    return all_achiev


@router.put('/update_achievements/{achiev_id}',
            response_model=AchievementsBase,
            description="Редактирование достижения по ID")
def update_achievements(achiev_id: int,
                        achiev: AchievementsBase,
                        db: Session = Depends(get_db)):
    achiev_new = db.query(Achievement).filter(
        Achievement.id == achiev_id).first()

    if not achiev_new:
        raise ACHIEV_EXCEPTION_404
    try:
        achiev_new.name = achiev.name
        db.commit()
        return achiev_new
    except SQLAlchemyError:
        raise SERVER_EXCEPTION_500


@router.delete('/delete_achievements/{achiev_id}',
               description="Удаление достижения по ID")
def delete_achievements(achiev_id: int, db: Session = Depends(get_db)):
    achiev = db.query(Achievement).filter(Achievement.id == achiev_id).first()
    if not achiev:
        raise ACHIEV_EXCEPTION_404
    try:
        db.delete(achiev)
        db.commit()
        return {"message": "Достижение удалено!"}
    except SQLAlchemyError:
        db.rollback()
        raise SERVER_EXCEPTION_500
