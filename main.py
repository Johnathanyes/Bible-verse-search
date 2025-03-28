from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, func

from contextlib import asynccontextmanager
from table_classes import *

import os
from dotenv import load_dotenv

load_dotenv()

VERSION_TABLES = {
    "niv": niv,
    "kjv": kjv,
    "esv": esv,
    "nlt": nlt,
    "nkjv": nkjv,
    "nasb": nasb,
}

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/{version}/get_verse")
async def root(session: SessionDep, version: str, book_name: str, chapter_num: int, verse_num: int):
    if version.lower() not in VERSION_TABLES:
        return HTTPException(status_code=404, detail="Invalid Bible Version Name")

    version_table = VERSION_TABLES[version.lower()]
    book_name = book_name.capitalize()
    statement = select(version_table).where(
        (version_table.book == book_name) & (version_table.chapter == chapter_num) & (version_table.verse == verse_num)
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

@app.get("/{version}/get_verses")
async def get_verses(session: SessionDep, version: str, book_name: str, chapter_num: int, verse_start: int, verse_end: int):
    if version.lower() not in VERSION_TABLES:
        return HTTPException(status_code=404, detail="Invalid Bible Version Name")
    
    version_table = VERSION_TABLES[version.lower()]
    book_name = book_name.capitalize()
    # Query all verses in a single database call
    statement = select(version_table).where(
        (version_table.book == book_name) &
        (version_table.chapter == chapter_num) &
        (version_table.verse >= verse_start) &
        (version_table.verse <= verse_end)
    )
    results = session.exec(statement).all()  # Fetch all matching verses

    if not results:
        raise HTTPException(status_code=404, detail=f'No verses found for {book_name} chapter {chapter_num}, verses {verse_start}-{verse_end}')
    
    # Convert results to JSON format
    list_of_verses = [
        {
            "book_num": verse.book_id,
            "book_name": verse.book,
            "chapter_num": verse.chapter,
            "verse_num": verse.verse,
            "text": verse.text
        }
        for verse in results
    ]

    return {"verses": list_of_verses}

@app.get("/{version}/get_chapter")
async def get_chapter(session: SessionDep, version: str, book_name: str, chapter_num: int):
    if version.lower() not in VERSION_TABLES:
        return HTTPException(status_code=404, detail="Invalid Bible Version Name")
    
    version_table = VERSION_TABLES[version.lower()]
    book_name = book_name.capitalize()
    statement = select(version_table).where(
        (version_table.book == book_name) &
        (version_table.chapter == chapter_num)
    )
    result = session.exec(statement).all()
    return_object = {
        "chapter": result
    }
    return return_object

@app.get("/{version}/get_random_verse")
async def get_random_verse(session: SessionDep, version: str):
    if version.lower() not in VERSION_TABLES:
        return HTTPException(status_code=404, detail="Invalid Bible Version Name")
    
    version_table = VERSION_TABLES[version.lower()]
    statement = select(version_table).order_by(
        func.random()
    )
    result = session.exec(statement).first()
    return_value = {
        "random_verse": result
    }
    return return_value
#http://127.0.0.1:8000/niv/get_verse?book_name=Genesis&chapter_num=1&verse_num=1