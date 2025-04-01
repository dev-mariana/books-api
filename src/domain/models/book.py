from sqlmodel import SQLModel, Field
import uuid

class Book(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field()
    description: str | None = Field()
    image_url: str | None = Field()
    author: str = Field()
    genre: str = Field()
    publication_year: int = Field()
