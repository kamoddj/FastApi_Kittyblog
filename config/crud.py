from fastapi.security import OAuth2PasswordBearer
from config.hashing import Hasher
from models.models import User
from models.shcemas import UserCreate
from sqlalchemy.orm import Session


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "8e054c0b7cf3c254b607a11cdb821d8560c5e2de94789a409c9b99414690d4de"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


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

# def authenticate_user(email: str, password: str, db: Session):
#     user = db.query(User).filter(User.email == email).first()
#     if not Hasher.verify_password(password, user.hashed_password):
#         return False
#     return User


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + datetime.timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = JWTError.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt