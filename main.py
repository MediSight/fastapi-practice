import mysql.connector
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import uuid
from uuid import UUID

db = mysql.connector.connect(   #MySQL 연결정보
    host = "localhost",
    user = "root",
    password = "391104",
    database = "bookshelf"
)

app = FastAPI()
#router = APIRouter()  #라우팅: 요청받은 URL을 해석하여 그에 맞는 기능을 실행하고 리턴, FastAPI에서는 APIRouter 클래스로 구현 가능하다
#app.include_router(,
#    prefix="/bookshelf",
#    tags=["bookshelf"]
#)

cursor = db.cursor(dictionary=True)  #cursor: DB에서 SELECT 쿼리문을 이용해 데이터를 읽으면, 해당 데이터의 위치를 가리켜 읽어올 수 있도록 한다. 
                                       #쿼리문을 보내고 다시 데이터를 받고, 데이터의 위치를 기억하는, 서버와의 통신 전반을 담당하는 객체?

#에러 이유, fetchall에서 타입 에러 발생, dict 아니면 json가 아니기에 발생한다는 듯. cursor에서 dictionary = True로 해도 해결 안됨. +) 직렬화 과정에서의 문제?? 무슨 소리?

def uuid_to_bin(uuid_str: str) -> bytes:
    return UUID(uuid_str).bytes

def bin_to_uuid(bin: bytes) -> UUID:
    return UUID(bytes=bin)

#async def search_book_by_title(title: str):  # ?????????
#    async with database.pool.acquire() as connection:
#        async with connection.cursor() as cursor:
#            query = "SELECT * FROM books WHERE title LIKE %s"
#            await cursor.execute(query, ('%' + title + '%',))
#            result = await cursor.fetchall()
#            return result

class Book(BaseModel):
    id: str
    title: str
    author: str
    description: Optional[str] = None
    published_date: Optional[str] = None

@app.get("/books/")
def get_book_all():
    query = "SELECT * FROM books"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@app.get("/books/{title}")
def get_book_title(title: str):
    query = "SELECT * FROM books WHERE title = {title}"
    cursor.execute(query)
    result = cursor.fetchall()
    if result is None:
      raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")
    return result

@app.post("/books/")
def create_book(book: Book):
    query = """
        INSERT INTO books (id, title, author, description, published_date)
        VALUES (UUID_TO_BIN(%s), %s, %s, %s, %s)
    """
    book_id = uuid.uuid4()
    values = (str(book_id), book.title, book.author, book.description, book.published_date)
    cursor.execute(query, values)  #MySQL 서버로 쿼리와 값을 전달
    db.commit()
    return {"message": "성공적으로 등록하였습니다.", "book_id": str(book_id)}

#UUID에 기초하여 탐색? 어떻게?

#@app.put("/books/{book_id}")
#def update_book(book_id: UUID, book: Book):
#    query = """
#        UPDATE books
#        SET title = %s, author = %s, description = %s, published_date = %s
#        WHERE id = %s
#    """
#    values = (book.title, book.author, book.description, book.published_date, str(book_id))
#    cursor.execute(query, values)
#    db.commit()
#   return {"message": "성공적으로 갱신되었습니다."}

@app.delete("/books/{title}")
def delete_book(title: str):
    query = "DELETE FROM books WHERE title = {title}"
    values = (str(title))
    cursor.execute(query, values)
    db.commit()
    return {"message": "성공적으로 삭제되었습니다."}
