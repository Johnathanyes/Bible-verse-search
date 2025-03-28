from sqlmodel import *

class niv(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str

class kjv(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str
class nasb(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str
class esv(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str
class nlt(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str
class nkjv(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str