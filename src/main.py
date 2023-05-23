from typing import Union, Literal, Optional
from fastapi import FastAPI
from prisma import Prisma
from pydantic import BaseModel


app = FastAPI()
db = Prisma()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


class User(BaseModel):
    email: str
    name: str


@app.post("/create/")
async def create_user(user: User, response_model=User) -> User:
    db_user = await db.user.create(
        data={
            "email": user.email,
            "name": user.name
        }
    )
    return user


@app.get("/users/{email}")
async def get_users(email: str):
    user = await db.user.find_unique(
        where={
            "email": email
        }
    )
    return {"email": user.email, "name": user.name, "id": user.id, "created_at": user.created_at, "updated_at": user.updated_at}
