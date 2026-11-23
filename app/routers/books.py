

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book as BookModel
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter()




# 1. GET: Display all books from SQLite
@router.get("/", response_model=list[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return db.query(BookModel).all()


# 2. GET: Display a book by ID from SQLite
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(BookModel).filter(
        BookModel.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


# 3. POST: Create a new book in SQLite
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(book: BookCreate, db: Session = Depends(get_db)):

    new_book = BookModel(**book.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book




# 4. PUT: Update complete book information in SQLite
@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    updated_book: BookCreate,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(
        BookModel.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    new_data = updated_book.model_dump()

    for key, value in new_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


# 5. PATCH: Update selected book information in SQLite
@router.patch("/{book_id}", response_model=BookResponse)
def partial_update_book(
    book_id: int,
    updated_data: BookUpdate,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(
        BookModel.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    changes = updated_data.model_dump(exclude_unset=True)

    for key, value in changes.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


# 6. DELETE: Delete a book from SQLite
@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(
        BookModel.id == book_id
    ).first()

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }
