from pydantic import BaseModel
from datetime import datetime 

class UserCreate(BaseModel):
    username:str 
    password:str 

class UserOut(BaseModel):
    id:int 
    username:str 
    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token:str 
    token_type:str 

class AskRequest(BaseModel):
    question:str

class AskResponse(BaseModel):
    question:str 
    generated_sql:str 
    result:list[dict]

class QueryLogOut(BaseModel):
    id:int 
    question:str
    generated_sql:str
    recorded_at:datetime
    class Config:
        from_attributes=True 
        