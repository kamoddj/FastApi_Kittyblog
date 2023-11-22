## Проект KittyBlog
### Технологии: Python, FastApi, SQLAlchemy, Alembic


## API приложение написанное с помощь FastApi. 

- Реализована аутентификация пользователя по JWT токену
- Атентифицированные пользователи могу добавлять котиков и достижения. Изменять и удалять их.
- Реализована валидация даты рождения и цвета котика.
- Для пользователей реализованы роли. Администратор может производить все CRUD операции, со всеми пользователями. Обычные пользователи только со своими записями.
- Документация к API доступна [здесь](http://127.0.0.1:8000/docs#/)
- Используется база Postgresql. Взаимодействует она с FastApi с помощью SQLAlchemy 2.0.


### Возможности проекта

Тут ты можешь регистрироваться и заводить котиков. Добавлять их достижения. Удалять и редактировать их.




### Запуск проекта на локальной машине:

- Клонировать репозиторий:
```
git clone git@github.com:kamoddj/FastApi_Kittyblog.git
```
-Устанавливаем зависимости 
```
pip install -r requirements.txt
```
-Запускаем проект
```
uvicorn main:app --reload
```
