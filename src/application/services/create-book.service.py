from infra.database.repositories import BooksRepository
from domain.models import Book

class CreateBookService:
    def __init__(self, repository: BooksRepository):
        self.repository = repository

    async def execute(self, book: Book):
        return await self.repository.create_book(book)