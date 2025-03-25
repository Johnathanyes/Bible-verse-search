from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

import os
from dotenv import load_dotenv

load_dotenv()

class niv(SQLModel, table=True):
    book_id: int = Field(primary_key=True)
    book: str
    chapter: int = Field(primary_key=True)
    verse: int = Field(primary_key=True)
    text: str

db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
postgresql_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/{db_name}'

engine = create_engine(postgresql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/niv/get_verse")
async def root(session: SessionDep, book_name: str, chapter_num: int, verse_num: int):
    statement = select(niv).where(
        (niv.book == book_name) & (niv.chapter == chapter_num) & (niv.verse == verse_num)
    )
    result = session.exec(statement).first()  # Use `.first()` if you expect only one verse
    if not result:
        raise HTTPException(status_code=404, detail="Could not find verse")
    verse_object = {
        "book_num": result.book_id,
        "book_name": result.book,
        "chapter_num": result.chapter,
        "verse_num": result.verse,
        "text": result.text
    }
    return verse_object

#http://127.0.0.1:8000/niv/get_verse?book_name=Genesis&chapter_num=1&verse_num=1