from sqlmodel import select
from src.infra.database.connection import Session
from domain.models import Book

class BookRepository:
    @staticmethod
    async def create_book(session: Session, book: Book):
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    @staticmethod
    async def get_books(session: Session):
        return session.exec(select(Book)).all()

    @staticmethod
    async def get_book(session: Session, book_id: str):
        return session.get(Book, book_id)

    @staticmethod
    async def update_book(session: Session, book_id: str, updated_book: Book):
        book = await BookRepository.get_book(session, book_id)
        if not book:
            raise Exception("Book not found")
        
        for field, value in updated_book.model_dump().items():
            setattr(book, field, value)
        session.commit()
        session.refresh(book)
        return book

    @staticmethod
    async def delete_book(session: Session, book_id: str):
        book = await BookRepository.get_book(session, book_id)
        if not book:
            raise Exception("Book not found")
        
        session.delete(book)
        session.commit()
