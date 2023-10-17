from database import Base
from sqlalchemy import Column, Integer, String
class ToDo(Base):
    __tablename__ = 'todo_list'
    id = Column(Integer, primary_key=True)
    task =  Column(String(50))