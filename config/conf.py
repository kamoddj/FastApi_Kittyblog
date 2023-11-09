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
