from database import Base 
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.sql import func

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    username=Column(String(100),unique=True,nullable=False)
    hashedpassword=Column(String(300),nullable=False)

class QueryLog(Base):
    __tablename__="queires"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    question=Column(String(500),nullable=False)
    generated_sql = Column(String(1000), nullable=True)
    recorded_at=Column(DateTime(timezone=True),server_default=func.now())
