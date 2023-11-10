from fastapi import FastAPI
from routers import cats, users, achivements
import auth


app = FastAPI(
    title="Cats api"
)

app.include_router(cats.router)
app.include_router(users.router)
app.include_router(achivements.router)
app.include_router(auth.router)
