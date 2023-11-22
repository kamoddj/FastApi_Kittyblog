from fastapi import FastAPI

import auth
from routers import achivements, cats, users

app = FastAPI(
    title="Cats api"
)

app.include_router(cats.router)
app.include_router(users.router)
app.include_router(achivements.router)
app.include_router(auth.router)
