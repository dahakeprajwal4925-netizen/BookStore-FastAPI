from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.models.book import Book
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):

    try:
        total_amount = 0
        order_items = []

        # Check each requested book
        for item in order_data.items:

            book = db.query(Book).filter(Book.id == item.book_id).first()

            if not book:
                raise HTTPException(
                    status_code=404,
                    detail=f"Book with ID {item.book_id} not found"
                )

            if book.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for book: {book.title}"
                )

            # Calculate item price
            item_total = book.price * item.quantity
            total_amount += item_total

            order_items.append({
                "book": book,
                "quantity": item.quantity,
                "price": book.price
            })

        # Create order
        new_order = Order(
            customer_name=order_data.customer_name,
            email=order_data.email,
            phone=order_data.phone,
            address=order_data.address,
            total_amount=total_amount,
            status="Pending"
        )

        db.add(new_order)
        db.flush()

        # Create order items and reduce stock
        for item in order_items:

            order_item = OrderItem(
                order_id=new_order.id,
                book_id=item["book"].id,
                quantity=item["quantity"],
                price=item["price"]
            )

            item["book"].stock -= item["quantity"]

            db.add(order_item)

        # Save everything together
        db.commit()
        db.refresh(new_order)

        return new_order

    except HTTPException:
        # Undo database changes if validation fails
        db.rollback()
        raise

    except SQLAlchemyError:
        # Undo database changes if a database error occurs
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Order could not be created due to a database error."
        )