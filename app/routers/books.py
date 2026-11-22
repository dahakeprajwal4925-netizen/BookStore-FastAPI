
from fastapi import APIRouter, HTTPException, status
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter()


# Temporary database (Python list)
BOOKS = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "John Smith",
        "category": "Programming",
        "price": 499,
        "stock": 10
    },
    {
        "id": 2,
        "title": "Learning FastAPI",
        "author": "David Brown",
        "category": "Technology",
        "price": 599,
        "stock": 5
    },
    {
        "id": 3,
        "title": "Clean Code",
        "author": "Robert Martin",
        "category": "Programming",
        "price": 699,
        "stock": 8
    }
]


# 1. GET: Display all books
@router.get("/", response_model=list[BookResponse])
async def get_all_books():
    return BOOKS


# 2. GET: Display a book by ID
@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int):

    for book in BOOKS:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


# 3. POST: Create a new book
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_book(book: BookCreate):

    new_book = book.model_dump()

    new_book["id"] = max(
        (item["id"] for item in BOOKS),
        default=0
    ) + 1

    BOOKS.append(new_book)

    return new_book


# 4. PUT: Update complete book information
@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, updated_book: BookCreate):

    for index, book in enumerate(BOOKS):

        if book["id"] == book_id:

            new_data = updated_book.model_dump()
            new_data["id"] = book_id

            BOOKS[index] = new_data

            return new_data

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


# 5. PATCH: Update selected book information
@router.patch("/{book_id}", response_model=BookResponse)
async def partial_update_book(
    book_id: int,
    updated_data: BookUpdate
):

    for book in BOOKS:

        if book["id"] == book_id:

            changes = updated_data.model_dump(
                exclude_unset=True
            )

            book.update(changes)

            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


# 6. DELETE: Delete a book
@router.delete("/{book_id}")
async def delete_book(book_id: int):

    for index, book in enumerate(BOOKS):

        if book["id"] == book_id:

            BOOKS.pop(index)

            return {
                "message": "Book deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
