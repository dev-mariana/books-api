from fastapi import FastAPI, HTTPException, Depends
import uuid
from typing import  List
from sqlmodel import create_engine, SQLModel, Field, Session, select
from dotenv import load_dotenv
import os


load_dotenv()

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field()
    description: str | None = Field()
    image_url: str | None = Field()
    author: str = Field()
    genre: str = Field()
    publication_year: int = Field()


app = FastAPI()   

db = os.getenv("DB_URL")

engine = create_engine(db)
SQLModel.metadata.create_all(engine)

def get_session():
       with Session(engine) as session:
           yield session
      

@app.get("/")
async def root():
    return {"message": "Welcome to the Books API!"}

@app.post("/api/books", response_model=Book)
async def create_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)

    return book

@app.get("/api/books", response_model=list[Book])
async def get_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()

    return books

@app.get("/api/books/{book_id}", response_model=Book)
async def get_book(book_id: uuid.UUID, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
    

@app.patch("/api/books/{book_id}", response_model=Book)
async def update_book(book_id: uuid.UUID, updated_book: Book, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in updated_book.model_dump().items():
            setattr(book, field, value)
    session.commit()
    session.refresh(book)
    return book

@app.delete("/api/books/{book_id}", status_code=204)
async def delete_book(book_id: uuid.UUID, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    session.delete(book)
    session.commit()
     
    