from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE

class BookTable(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key = True, autoincrement = True)
    book_title = Column(String(20), nullable = False)
    author = Column(String(20), nullable = False)
    price = Column(Integer)

class Book(BaseModel):
    book_id: int
    book_title: str
    author: str
    price: int
