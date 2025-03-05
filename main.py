from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import  List

app = FastAPI()

class Book(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str | None 
    image_url: str
    author: str
    genre: str
    publication_year: int

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
async def get_book(book_id: UUID):
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")

@app.patch("/api/books/{book_id}")
async def update_book(book_id: UUID, updated_book: Book):
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
async def delete_book(book_id: UUID):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")