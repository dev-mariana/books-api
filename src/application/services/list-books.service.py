from infra.database.repositories import BooksRepository
from domain.models import Book

class ListBooksService:
    def __init__(self, repository: BooksRepository):
        self.repository = repository

    async def execute(self):
        return await self.repository.get_books()