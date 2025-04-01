from infra.database.repositories import BooksRepository
from domain.models import Book

class UpdateBookService:
    def __init__(self, repository: BooksRepository):
        self.repository = repository

    async def execute(self, book_id: str, updated_book: Book):
        book = await self.repository.get_book(book_id)

        return await self.repository.get_books(book_id, updated_book)