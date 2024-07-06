from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Todo
import redis
from dotenv import dotenv_values
from models import Todo, User
import json
import uuid
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter()

config = dotenv_values(".env")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

r = redis.Redis(host='redis-11767.c325.us-east-1-4.ec2.redns.redis-cloud.com', port=11767, password=config["PASSWORD"], decode_responses=True)

try:
    version = r.info()['redis_version']
    print(f"Version du serveur Redis: {version}")
except Exception as e:
    print("Impossible de se connecter au serveur Redis:", e)

##function to check if user already exist
def getExistingUser():
    name = []
    for key in r.scan_iter("User:*"):
        user = r.json().get(key)
        name.append(user['name'])

    return name

##Create a new User
@router.post("/create/user")
async def createTodo(body: User):
    myuuid = uuid.uuid4()
    
    name = getExistingUser()
    exist = body.name in name
    if not exist:
        data = User(
        id = str(myuuid),
        name=body.name,
        email=body.email,
        password=pwd_context.hash(body.password)
    )
        user = jsonable_encoder(data)
        res = r.json().set(f'User:{myuuid}', '$', user)
        return {"message":  res}
    else:
        raise HTTPException(status_code=401, detail="User already exist")
    

##Create a new Todo
@router.post("/create/todo")
async def createTodo(body: Todo):
    myuuid = uuid.uuid4()
    data = Todo(
        id = str(myuuid),
        name=body.name,
        description=body.description,
    )
    todo = jsonable_encoder(data)
    res = r.json().set(f'Todo:{myuuid}', '$', todo)
    return {"message":  res}

##get a specific Todo
@router.get("/get/todo/{id}")
async def getSpecifiqueTodo(id: str):
    Todo=r.json().get(f'Todo:{id}')
    if Todo:
        return Todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

#Get all todos
@router.get("/todo")
async def all_etagere():
    all_todo = []
    for key in r.scan_iter("Todo:*"):
        todo = r.json().get(key)
        all_todo.append(todo)
        
    return all_todo

##delete a Todo 
@router.delete("/delete/todo/{id}")
async def deleteTodo(id: str):
    key = f'Todo:{id}'
    try:
        if key:
            Todo = r.json().forget(key)
            return "delete successfully"
        else:
            raise HTTPException(status_code=404, detail="Todo not found")
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Internal Server Error")

##Uplaod todo a Todo
@router.put("/update/todo/{id}")
async def updateTodo(id: str, body: Todo):
    key = f'Todo:{id}'
    td = r.json().get(key)

    if td:
        data = Todo(
            id=id,
            name=body.name,
            description=body.description,
        )
        
        new_data = jsonable_encoder(data)
        update_data = r.json().set(f'Todo:{id}', '$', new_data)
        
        return "Todo update Successfully"
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

##Update the status 
@router.put("/update/todo/status/{id}")
async def updateTodo(id: str):
    key = f'Todo:{id}'
    td = r.json().get(key)

    if td:
        td['status'] = "finished"
        new_data = jsonable_encoder(td)
        update_data = r.json().set(f'Todo:{id}', '$', new_data)
        return update_data
    else:
        raise HTTPException(status_code=404, detail="Todo not found")