from fastapi import FastAPI, HTTPException
import uuid
from typing import  List
from sqlmodel import create_engine, SQLModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    description: str | None = Field(index=True)
    image_url: str | None = Field(index=True)
    author: str = Field(index=True)
    genre: str = Field(index=True)
    publication_year: int = Field(index=True)

database_url = os.getenv("DATABASE_URL")   

engine = create_engine(database_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)   

create_db_and_tables()    

books: List[Book] = []    

@app.get("/")
async def root():
    return {"message": "Welcome to the Books API!"}

@app.post("/api/books")
async def create_book(book: Book):
    books.append(book)
    return book

@app.get("/api/books")
async def get_books():
    return books

@app.get("/api/books/{book_id}")
async def get_book(book_id: uuid.UUID):
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.patch("/api/books/{book_id}")
async def update_book(book_id: uuid.UUID, updated_book: Book):
    for book in books:
        if book.id == book_id:
            book.title = updated_book.title
            book.description = updated_book.description
            book.image_url = updated_book.image_url
            book.author = updated_book.author
            book.genre = updated_book.genre
            book.publication_year = updated_book.publication_year
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/api/books/{book_id}")
async def delete_book(book_id: uuid.UUID):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")