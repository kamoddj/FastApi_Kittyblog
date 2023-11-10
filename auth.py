from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import crud, exceptions
from models.database import get_db
from models.models import User
from models.shcemas import Token


router = APIRouter(
    prefix='/login',
    tags=['login'],
)


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise exceptions.UNAUTORIZED_EXCEPTION_401
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={'sub': user.email,
              'other_custom_data': [1, 2, 3, 4]},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/simple')
def sample_jwt(current_user: User = Depends(crud.get_current_user)):
    return {"Success": True, "current_user": current_user}
