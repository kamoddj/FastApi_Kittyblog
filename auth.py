from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.exceptions import UNAUTORIZED_EXCEPTION_401
from config.hashing import Hasher
from config.crud import (get_user_by_email, SECRET_KEY,
                         ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                         oauth2_scheme)
from models.database import get_db
from models.models import User
from models.shcemas import Token


router = APIRouter(
    prefix='/login',
    tags=['login'],
)


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise UNAUTORIZED_EXCEPTION_401
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email,
              'other_custom_data': [1, 2, 3, 4]},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise UNAUTORIZED_EXCEPTION_401
    except JWTError:
        raise UNAUTORIZED_EXCEPTION_401
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise UNAUTORIZED_EXCEPTION_401
    return user


@router.get('/simple')  #, response_model=UserUpdate
def sample_jwt(current_user: User = Depends(get_current_user)):
    return {"Success": True, "current_user": current_user}
