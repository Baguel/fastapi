from typing import Optional, Literal
from pydantic import BaseModel, Field
import datetime

class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    
class Todo(BaseModel):
    id: str
    name: str
    description: str
    status:  Literal['Started', 'finished'] | Optional[str] = 'Started'
    create_at: str = datetime.datetime.now()

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserInDB(User):
    password: str