from loguru import logger
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import verify_token
from app.core.db.session import get_db
from app.books.models import Book as BookModel, Author as AuthorModel
from app.books.schema import BookSchema, AuthorSchema


router = APIRouter(dependencies=[Depends(verify_token)])


# -------------------------------
# Author Endpoints
# -------------------------------
@router.get("/authors", status_code=200)
async def get_authors(db: Session = Depends(get_db)):
    """
    Gets all authors listed in the database.

    Returns:
        list: An array of author objects.
    """
    return db.query(AuthorModel).all()


@router.post("/authors", status_code=201)
async def add_author(payload: AuthorSchema, db: Session = Depends(get_db)):
    """
    Adds an author in the database.

    Returns:
        Object: Same payload with 201 status code on success.
    """
    new_author = AuthorModel(
        name=payload.name,
        age=payload.age
    )
    
    db.add(new_author)
    db.commit()
    
    logger.success("Added an author.")
    return payload


@router.put("/authors/{author_id}", status_code=201)
async def update_author(author_id: int, payload: AuthorSchema, db: Session = Depends(get_db)):
    """
    Updates the author object in the database.

    Raises:
        HTTPException: 404 if author id is not found.

    Returns:
        object: Updated author object with 201 status code.
    """
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    
    if not author:
        desc = "Author not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    author.name = payload.name
    author.age = payload.age
    db.commit()

    logger.success("Updated an author.")
    return author


@router.delete("/authors/{author_id}", status_code=204)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    """
    Deletes an author object from the database.

    Raises:
        HTTPException: 404 if author id is not found.

    Returns:
        Object: Deleted true with 204 status code.
    """
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    
    if not author:
        desc = "Author not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    db.delete(author)
    db.commit()

    logger.success("Deleted an author.")
    return {"Deleted": True}


# -------------------------------
# Book Endpoints
# -------------------------------
@router.get("/books", status_code=200)
async def get_books(db: Session = Depends(get_db)):
    """
    Gets all books listed in the database.

    Returns:
        list: An array of book objects.
    """
    return db.query(BookModel).all()


@router.post("/books", status_code=201)
async def add_book(payload: BookSchema, db: Session = Depends(get_db)):
    """
    Adds a book in the database.

    Returns:
        Object: Same payload with 201 status code on success.
    """
    author = db.query(AuthorModel).filter(AuthorModel.id == payload.author_id).first()
    
    if not author:
        desc = "Author not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    new_book = BookModel(
        title=payload.title,
        rating=payload.rating,
        author_id=payload.author_id
    )

    db.add(new_book)
    db.commit()

    logger.success("Added a book.")
    return payload


@router.put("/books/{book_id}", status_code=201)
async def update_book(book_id: int, payload: BookSchema, db: Session = Depends(get_db)):
    """
    Updates the book object in the database.

    Raises:
        HTTPException: 404 if book id is not found.

    Returns:
        object: Updated book object with 201 status code.
    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        desc = "Book not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    author = db.query(AuthorModel).filter(AuthorModel.id == payload.author_id).first()

    if not author:
        desc = "Author not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    book.title = payload.title
    book.rating = payload.rating
    book.author_id = payload.author_id
    db.commit()

    logger.success("Updated a book.")
    return book


@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Deletes a book object from the database.

    Raises:
        HTTPException: 404 if book id is not found.

    Returns:
        Object: Deleted true with 204 status code.
    """
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        desc = "Book not found"
        logger.error(desc)
        raise HTTPException(status_code=404, detail=desc)

    db.delete(book)
    db.commit()

    logger.success("Deleted a book.")
    return {"Deleted": True}
