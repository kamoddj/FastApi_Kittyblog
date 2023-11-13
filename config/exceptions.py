from fastapi import HTTPException, status
# Исключения

SERVER_EXCEPTION_500 = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Упс, что-то пошло не так!"
)

ACHIEV_EXCEPTION_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Достижение не найдено"
)

CAT_EXCEPTION_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Котик не найден"
)

USER_EXCEPTION_404 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Пользователь не найден"
)

UNAUTORIZED_EXCEPTION_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь не авторизован",
    headers={"WWW-Authenticate": "Bearer"}
)

EMAIL_EXCEPTION_409 = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email уже существует"
)

ACTIVE_EXCEPTION_409 = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь не активен"
)

STRANER_ID_EXEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Использованы неверные данные"
)
