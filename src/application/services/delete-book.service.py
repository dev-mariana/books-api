from infra.database.repositories import BooksRepository
from domain.models import Book

class DeleteBookService:
    def __init__(self, repository: BooksRepository):
        self.repository = repository

    async def execute(self, book_id: str):
        await self.repository.get_book(book_id)

        await self.repository.delete_book(book_id)