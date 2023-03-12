# FastAPI Practice
from fastapi import FastAPI, requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from starlette.middleware.cors import CORSMiddleware

from db import session
from model import BookTable, Book


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get("/")
def root():
    return {"Hello":"This is My Bookshelf"}

@app.get('/books')
def get_books():
    books = session.query(BookTable).all()
    return books


@app.get('/books/{book_id}')
def get_book(book_id: int):
    book = session.query(BookTable).filter(BookTable.book_id == book_id).first()

    return book

@app.post('/books')
def create_book(book_title: str, author: str, price: int):
    book = BookTable()
    book.book_title = book_title
    book.author = author
    book.price = price

    session.add(book)
    session.commit()

    return f"{book_title} created!"

@app.put('/books')
def update_books(books: List[Book]):
    
    for i in books:
        book = session.query(BookTable).filter(BookTable.book_id == i.book_id).first()
        book.book_title = i.book_title
        book.author = i.author
        book.price = i.price
        session.commit()
    
    return f"{i.book_title} updated!"

@app.delete('/books')
def delete_book(book_id: int):
    book = session.query(BookTable).filter(BookTable.book_id == book_id).delete()
    session.commit()

    return "Delete Completed!"
