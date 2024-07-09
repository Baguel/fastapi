from fastapi import FastAPI, HTTPException
from dotenv import dotenv_values
import redis
from models import Todo
from fastapi.encoders import jsonable_encoder
import json
import uuid
import todo

app = FastAPI()

app.include_router(todo.router)