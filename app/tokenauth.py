from fastapi import APIRouter, Body, Request, Response, HTTPException, status
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

config = dotenv_values(".env")

def token_response(token: str):
    return {
        "token": token
    }

def sign_token(user: object):
    playload = {
        "user": user,
        "expires": config["ACCESS_TOKEN_EXPIRE_MINUTES"]
    }
    token = jwt.encode(playload, config["SECRET_KEY"], algorithm="HS256")
    return token_response(token)
    
def decode_token(token: str):
    try:
        decodetoken = jwt.decode(token, config['SECRET_KEY'], algorithms=config["ALGORITHM"])
        return decodetoken 
    except:
        return {}
    
