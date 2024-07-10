from typing import Optional, Literal, ClassVar
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
    user_id: str
    create_at: ClassVar[str] = datetime.datetime.now()

class login(BaseModel):
    email: str
    password: str
