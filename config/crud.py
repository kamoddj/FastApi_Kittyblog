from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.exceptions import UNAUTORIZED_EXCEPTION_401
from config.hashing import Hasher
from models.database import get_db
from models.models import User
from models.shcemas import UserCreate
from sqlalchemy.orm import Session


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "8e054c0b7cf3c254b607a11cdb821d8560c5e2de94789a409c9b99414690d4de"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


# FastApi /users
def create_new_user(user: UserCreate, db: Session):
    user_model = User(
        name=user.name.title(),
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.hashed_password)
    )
    return user_model


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


# FastApi /login
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
