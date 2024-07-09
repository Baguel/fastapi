from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from models import Todo, login
import redis
from dotenv import dotenv_values
from models import Todo, User
import json
import uuid
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
import time
import jwt
from tokenauth import sign_token, decode_token
from auth import JWTBearer
from db import *

router = APIRouter()

config = dotenv_values(".env")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


##function to check if user already exist
def getExistingUser():
    li = []
    for key in r.scan_iter("User:*"):
        user = r.json().get(key)
        li.append({"email" : user['email'], "id": user['id']})
    
    return li


##Create a new User
@router.post("/create/user")
async def createUser(body: User):
    mail = []
    myuuid = uuid.uuid4()
    
    li = getExistingUser()
    for user in li:
        mail.append(user['email'])
 
    exist = body.email in mail 
    
    if not exist:
        data = User(
        id = str(myuuid),
        name=body.name,
        email=body.email,
        password=pwd_context.hash(body.password)
    )
        user = jsonable_encoder(data)
        res = r.json().set(f'User:{myuuid}', '$', user)
        return res
    else:
        raise HTTPException(status_code=401, detail="User already exist")
     
##Login a user
@router.post("/login")
async def loginUser(body: login):
    mail = []
    id = ""
    li = getExistingUser()
    for user in li:
        if body.email == user['email']:
            id = user['id']
 
    res = r.json().get(f'User:{id}')

    if res:
        check = pwd_context.verify(body.password, res["password"])
        if check:
            token = sign_token(res)
            return token
        else:
            raise HTTPException(status_code=401, detail="Wrong Password")
    else:
            raise HTTPException(status_code=404, detail="user doesn't exist")


##Create a new Todo
@router.post("/create/todo")
async def createTodo(body: Todo, user : dict = Depends(JWTBearer())):
    myuuid = uuid.uuid4()
    data = Todo(
        id = str(myuuid),
        name=body.name,
        description=body.description,
        user_id = user["id"]
    )
    todo = jsonable_encoder(data)
    res =  r.json().set(f'Todo:{myuuid}', '$', todo)
    if res:
        return {"message":  res}
    else:
        raise HTTPException(status_code=200, detail="There is no todo")

##get a specific Todo
@router.get("/get/todo/{id}")
async def getSpecifiqueTodo(id: str, user : dict = Depends(JWTBearer())):
    Todo =  r.json().get(f'Todo:{id}')
    if Todo:
        return Todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

#Get all todo
@router.get("/todo")
async def all_todos(user : dict = Depends(JWTBearer())):
    all_todo = []
    for key in r.scan_iter("Todo:*"):
        todo =  r.json().get(key)
        all_todo.append(todo)
    
    if all_todo:
        return all_todo
    else:
        raise HTTPException(status_code=404, detail="No Todo Found")

##delete a Todo 
@router.delete("/delete/todo/{id}")
async def deleteTodo(id: str, user : dict = Depends(JWTBearer())):
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
async def updateTodo(id: str, body: Todo, user : dict = Depends(JWTBearer())):
    key = f'Todo:{id}'
    td = r.json().get(key)
    try: 
        if td:
            data = Todo(
                id=id,
                name=td['name'],
                description=td['description'],
            )          
            new_data = jsonable_encoder(data)
            update_data = r.json().set(f'Todo:{id}', '$', new_data)
            
            return update_data
        else:
            raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

##Update the status of todo
@router.put("/update/todo/status/{id}")
async def updateTodo(id: str, user : dict = Depends(JWTBearer())):
    key = f'Todo:{id}'
    td = r.json().get(key)
    try:
        if td:
            td['status'] = "finished"
            new_data = jsonable_encoder(td)
            update_data = r.json().set(f'Todo:{id}', '$', new_data)
            return update_data
        else:
            raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")