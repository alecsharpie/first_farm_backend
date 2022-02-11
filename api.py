from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000"
]  # This will eventually be changed to only the origins you will use once it's deployed, to secure the app a bit more.

app = FastAPI()

import pymongo

from model import *
#import motor.motor_asyncio
from dotenv import dotenv_values
import os

from http.client import HTTPException

config = dotenv_values(".env")

DATABASE_URI = config.get("DATABASE_URI")

if os.getenv("DATABASE_URI"):
    DATABASE_URI = os.getenv(
        "DATABASE_URI"
    )  #ensures that if we have a system environment variable, it uses that instead

#client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

client = pymongo.MongoClient(DATABASE_URI)
db = client.test

database = client.TodoDatabase
collection = database.todos


def fetch_all_todos():
    todos = []
    cursor = collection.find()
    for doc in cursor:
        todos.append(Todo(**doc))
    return todos


async def fetch_one_todo(nanoid):
    doc = collection.find_one({"nanoid": nanoid}, {"_id": 0})
    return await doc


async def create_todo(todo):
    doc = todo.dict()
    collection.insert_one(doc)
    result = fetch_one_todo(todo.nanoid)
    return await result


async def change_todo(nanoid, title, desc, checked):
    await collection.update_one(
        {"nanoid": nanoid},
        {"$set": {
            "title": title,
            "desc": desc,
            "checked": checked
        }})
    result = await fetch_one_todo(nanoid)
    return result


async def remove_todo(nanoid):
    await collection.delete_one({"nanoid": nanoid})
    return True


app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get('/')
def get_root():
    return {"Ping": "Pong"}


@app.get("/api/get-todo/{nanoid}", response_model=Todo)
async def get_one_todo(nanoid):
    todo = await fetch_one_todo(nanoid)
    if not todo: raise HTTPException(404)
    return todo


@app.get("/api/get-todo")
def get_todos():
    todos = fetch_all_todos()
    if not todos: raise HTTPException(404)
    return todos


@app.post("/api/add-todo", response_model=Todo)
async def add_todo(todo: Todo):
    result = await create_todo(todo)
    if not result: raise HTTPException(400)
    return result


@app.put("/api/update-todo/{nanoid}", response_model=Todo)
async def update_todo(todo: Todo):
    result = await change_todo(todo.nanoid, todo.title, todo.desc,
                               todo.checked)
    if not result: raise HTTPException(400)
    return result


@app.delete("/api/delete-todo/{nanoid}")
async def delete_todo(nanoid):
    result = await remove_todo(nanoid)
    if not result: raise HTTPException(400)
    return result
