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
from tokenauth import sign_token


config = dotenv_values(".env")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

r = redis.Redis(host='redis-11767.c325.us-east-1-4.ec2.redns.redis-cloud.com', port=11767, password=config["PASSWORD"], decode_responses=True)

try:
    version = r.info()['redis_version']
    print(f"Version du serveur Redis: {version}")
except Exception as e:
    print("Impossible de se connecter au serveur Redis:", e)