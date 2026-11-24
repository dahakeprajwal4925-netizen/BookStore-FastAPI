
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book as BookModel
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter()


# 1. GET: Search, Filter and Sort books
@router.get("/", response_model=list[BookResponse])
def get_all_books(
    search: str | None = None,
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    sort_by: str = Query(default="id", pattern="^(id|title|price|stock)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(BookModel)

    # Search by title or author
    if search:
        query = query.filter(
            BookModel.title.ilike(f"%{search}%") |
            BookModel.author.ilike(f"%{search}%")
        )

    # Filter by category
    if category:
        query = query.filter(
            BookModel.category.ilike(category)
        )

    # Filter by minimum price
    if min_price is not None:
        query = query.filter(BookModel.price >= min_price)

    # Filter by maximum price
    if max_price is not None:
        query = query.filter(BookModel.price <= max_price)

    # Sorting
    sort_column = getattr(BookModel, sort_by)

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.offset(skip).limit(limit).all()


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
