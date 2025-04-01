from infra.database.repositories import BooksRepository
from domain.models import Book

class ListBookByIdService:
    def __init__(self, repository: BooksRepository):
        self.repository = repository

    async def execute(self, book_id: str):
        return await self.repository.get_book(book_id)